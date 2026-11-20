#!/usr/bin/env python3
"""Surveille le serveur OpenWISP et alerte sur Discord.

Vérifie que la page de connexion de l'admin OpenWISP répond HTTP 200, puis
délègue l'envoi du message à `ops/discord_alert.py`.

Usage :
    python3 ops/check_server.py            # vérifie et envoie l'alerte
    python3 ops/check_server.py --dry-run  # vérifie sans envoyer

Codes de sortie :
    0  serveur en ligne (alerte envoyée)
    1  serveur hors ligne (alerte envoyée)
    2  échec de l'envoi de l'alerte Discord
    3  erreur d'exécution (option invalide, etc.)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# La racine https://radius.wavefi.tech/ renvoie 404 (l'application Django
# n'expose pas de page d'accueil). La page de connexion de l'admin OpenWISP
# renvoie bien 200 et atteste que nginx + l'application répondent.
DEFAULT_URL = "https://radius.wavefi.tech/admin/login/"
EXPECTED_STATUS = 200
DEFAULT_TIMEOUT = 15.0
DEFAULT_ATTEMPTS = 2
RETRY_DELAY = 3.0

USER_AGENT = "WaveFi-OpenWISP-Monitor/1.0"
ALERT_SCRIPT = Path(__file__).resolve().parent / "discord_alert.py"

MESSAGE_ONLINE = "✅ [WaveFi] Statut : Serveur OpenWISP en ligne."
MESSAGE_OFFLINE = "🚨 [WaveFi] ALERTE : Serveur OpenWISP HORS LIGNE."


def configure_stdio() -> None:
    """Évite les erreurs d'encodage quand cron tourne en locale C/POSIX."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def now_tahiti() -> datetime:
    """Heure de Tahiti (UTC-10, sans heure d'été), avec repli en UTC."""
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("Pacific/Tahiti"))
    except Exception:  # tzdata absente ou zone inconnue
        return datetime.now(timezone.utc)


def check_once(url: str, timeout: float) -> tuple[bool, str]:
    """Effectue une requête et renvoie (succès, détail lisible)."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            response.read(2048)
        if status == EXPECTED_STATUS:
            return True, f"HTTP {status}"
        return False, f"HTTP {status} (attendu : {EXPECTED_STATUS})"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code} {exc.reason}".strip()
    except urllib.error.URLError as exc:
        return False, f"injoignable ({exc.reason})"
    except TimeoutError:
        return False, f"délai dépassé ({timeout:g} s)"
    except OSError as exc:
        return False, f"erreur réseau ({exc})"


def check(
    url: str,
    timeout: float = DEFAULT_TIMEOUT,
    attempts: int = DEFAULT_ATTEMPTS,
) -> tuple[bool, str]:
    """Vérifie l'URL, avec une seconde tentative pour éviter les faux positifs."""
    ok, detail = False, "aucune tentative"
    for attempt in range(1, attempts + 1):
        ok, detail = check_once(url, timeout)
        if ok or attempt == attempts:
            break
        time.sleep(RETRY_DELAY)
    return ok, detail


def send_alert(
    message: str,
    alert_script: Path = ALERT_SCRIPT,
    timeout: float = 90.0,
) -> bool:
    """Appelle discord_alert.py avec le message demandé."""
    try:
        result = subprocess.run(
            [sys.executable, str(alert_script), message],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
    except subprocess.TimeoutExpired:
        print(f"Discord : délai dépassé après {timeout:g} s.", file=sys.stderr)
        return False
    except OSError as exc:
        print(f"Discord : impossible d'appeler {alert_script} ({exc}).", file=sys.stderr)
        return False

    if result.stdout.strip():
        print(result.stdout.strip(), flush=True)
    if result.returncode != 0:
        print(
            f"Discord : échec de l'envoi (code {result.returncode}) "
            f"{result.stderr.strip()}",
            file=sys.stderr,
        )
        return False
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Surveille OpenWISP et alerte sur Discord.",
        epilog=(
            "Par défaut : vérifie "
            f"{DEFAULT_URL} et appelle ops/discord_alert.py."
        ),
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="URL à surveiller.")
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Délai par requête en secondes (défaut : {DEFAULT_TIMEOUT:g}).",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=DEFAULT_ATTEMPTS,
        help=f"Nombre de tentatives (défaut : {DEFAULT_ATTEMPTS}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Vérifie sans envoyer de message Discord.",
    )
    parser.add_argument(
        "--alert-script",
        type=Path,
        default=ALERT_SCRIPT,
        help="Script d'envoi (défaut : ops/discord_alert.py).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = parse_args(argv)
    try:
        if args.timeout <= 0:
            raise ValueError("--timeout doit être strictement positif.")
        if args.attempts < 1:
            raise ValueError("--attempts doit être au moins égal à 1.")
        if not args.alert_script.is_file():
            raise ValueError(f"script d'alerte introuvable : {args.alert_script}")
    except ValueError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 3

    ok, detail = check(args.url, args.timeout, args.attempts)
    stamp = now_tahiti().isoformat(timespec="seconds")
    state = "EN LIGNE" if ok else "HORS LIGNE"
    print(f"{stamp} {state} — {detail} — {args.url}", flush=True)

    if args.dry_run:
        return 0 if ok else 1

    message = MESSAGE_ONLINE if ok else MESSAGE_OFFLINE
    if not send_alert(message, args.alert_script):
        return 2
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
