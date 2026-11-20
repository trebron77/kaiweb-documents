#!/usr/bin/env python3
"""Surveille l'API FenuaFact : service HTTP **et** accès à la base.

Usage :
    python3 check_health.py                # vérifie et alerte si changement d'état
    python3 check_health.py --dry-run      # n'envoie aucune alerte
    HEALTH_URL=... python3 check_health.py # cible une autre URL

États possibles :
    OK      — API et base répondent
    API_KO  — l'API ne répond pas (service arrêté, nginx, certificat…)
    DB_KO   — l'API répond mais la base refuse la clé (rotation ratée, clé révoquée…)

Le script n'alerte que sur changement d'état pour éviter de saturer le canal.
Dépendances : bibliothèque standard uniquement.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
API_DIR = Path("/var/www/fenuafact-api")
DEFAULT_URL = "https://api.fenuafact.com/health"
DEFAULT_ENV = HERE / "discord.env"
STATE_FILE = HERE / ".health_state"
TIMEOUT = 10.0


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def check_api(url: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", "replace")
            return response.status == 200 and '"ok"' in body, f"HTTP {response.status} — {body[:120]}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def check_db() -> tuple[bool, str]:
    """Vérifie que la clé secrète Supabase est acceptée (lecture d'une ligne)."""
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_KEY", "")
    if not url or not key:
        return True, "base non configurée (ignorée)"
    request = urllib.request.Request(
        f"{url}/rest/v1/tenants?select=id&limit=1",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            response.read()
            return response.status == 200, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, f"HTTP {exc.code} — clé refusée"
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def alert(message: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] alerte non envoyée : {message}")
        return
    webhook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        print("DISCORD_WEBHOOK_URL absente : alerte non envoyée", file=sys.stderr)
        return
    payload = json.dumps(
        {
            "username": os.environ.get("DISCORD_ALERT_USERNAME", "FenuaFact Alertes"),
            "content": message[:2000],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        webhook, data=payload, headers={"Content-Type": "application/json", "User-Agent": "FenuaFact-Alerts/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            response.read()
    except Exception as exc:
        print(f"Échec de l'alerte Discord : {exc}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--env", default=str(DEFAULT_ENV))
    parser.add_argument("--api-env", default=str(API_DIR / ".env"))
    args = parser.parse_args()

    load_env(Path(args.env))
    load_env(Path(args.api_env))  # URL et clé Supabase

    url = os.environ.get("HEALTH_URL", DEFAULT_URL)
    api_ok, api_detail = check_api(url)

    if api_ok:
        db_ok, db_detail = check_db()
        etat = "OK" if db_ok else "DB_KO"
    else:
        db_ok, db_detail = False, "non testée"
        etat = "API_KO"

    previous = STATE_FILE.read_text(encoding="utf-8").strip() if STATE_FILE.exists() else None
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{stamp} {etat} {url} api={api_detail} db={db_detail}")

    changed = previous != etat
    STATE_FILE.write_text(etat, encoding="utf-8")

    if etat == "OK" and previous in ("API_KO", "DB_KO"):
        alert(f"✅ **FenuaFact** : de nouveau opérationnel (API + base).", args.dry_run)
    elif etat == "API_KO" and changed:
        alert(
            "🔴 **FenuaFact** : l'API ne répond plus.\n"
            f"`{url}` → {api_detail}\n"
            "Vérifier : `systemctl status fenuafact` puis `journalctl -u fenuafact -n 50`.",
            args.dry_run,
        )
    elif etat == "DB_KO" and changed:
        alert(
            "🟠 **FenuaFact** : l'API répond mais **la base la refuse**.\n"
            f"Base → {db_detail}\n"
            "Vérifier `SUPABASE_KEY` dans `/var/www/fenuafact-api/.env` "
            "(rotation de clé incomplète ?).",
            args.dry_run,
        )
    elif etat != "OK":
        print("  (incident déjà signalé, pas de nouvelle alerte)")

    return 0 if etat == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
