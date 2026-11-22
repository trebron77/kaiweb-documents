#!/usr/bin/env python3
"""Contrôle de santé du VPS WaveFi — alerte Discord.

À exécuter **sur le serveur** `radius.wavefi.tech`. Vérifie ce qu'un contrôle
externe ne peut pas voir : disque, mémoire, swap, mises à jour en attente,
service RADIUS. N'envoie un message **que s'il y a un problème** : pas de bruit
quotidien.

Usage :
    python3 check_vps.py                # contrôle silencieux (alerte si problème)
    python3 check_vps.py --dry-run      # affiche le rapport sans envoyer
    python3 check_vps.py --heartbeat    # force l'envoi du rapport complet

Le webhook est lu dans ce fichier `~/.wavefi.env` (une ligne) :
    DISCORD_WEBHOOK=https://discord.com/api/webhooks/...

Codes de sortie :
    0  tout va bien (ou alerte envoyée)
    1  au moins un seuil dépassé
    2  échec d'envoi de l'alerte Discord
    3  erreur d'exécution
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# --- seuils -----------------------------------------------------------------
DISK_WARN = 80.0        # % d'occupation
DISK_CRIT = 90.0
RAM_MIN_FREE_MB = 300   # mémoire réellement disponible
SWAP_WARN = 50.0        # % du swap utilisé
UPDATES_WARN = 20       # mises à jour en attente
PORTAL_URL = "https://radius.wavefi.tech/admin/login/"
ENV_FILE = Path.home() / ".wavefi.env"


def now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# --- collecte ---------------------------------------------------------------
def check_disk() -> tuple[str, bool, bool, str]:
    """(nom, ok, critique, détail)"""
    try:
        u = shutil.disk_usage("/")
    except OSError as exc:
        return ("Disque", False, True, f"illisible ({exc})")
    pct = u.used / u.total * 100
    free_gb = u.free / 1024**3
    ok = pct < DISK_WARN
    crit = pct >= DISK_CRIT
    return ("Disque", ok, crit, f"{pct:.0f} % utilisé — {free_gb:.1f} Go libres")


def read_meminfo() -> dict[str, int]:
    info: dict[str, int] = {}
    with open("/proc/meminfo", encoding="ascii") as fh:
        for line in fh:
            key, _, rest = line.partition(":")
            num = rest.strip().split()[0] if rest.strip() else "0"
            try:
                info[key] = int(num)  # en Ko
            except ValueError:
                info[key] = 0
    return info


def check_memory() -> list[tuple[str, bool, bool, str]]:
    try:
        mi = read_meminfo()
    except OSError as exc:
        return [("Mémoire", False, True, f"illisible ({exc})")]
    total = mi.get("MemTotal", 0) // 1024
    avail = (mi.get("MemAvailable", 0)) // 1024
    swap_t = mi.get("SwapTotal", 0) // 1024
    swap_f = mi.get("SwapFree", 0) // 1024

    rows = []
    rows.append((
        "Mémoire",
        avail >= RAM_MIN_FREE_MB,
        avail < 150,
        f"{avail} Mo disponibles sur {total} Mo",
    ))
    if swap_t > 0:
        swap_used_pct = (swap_t - swap_f) / swap_t * 100
        rows.append((
            "Swap",
            swap_used_pct < SWAP_WARN,
            swap_used_pct >= 90,
            f"{swap_used_pct:.0f} % utilisé ({swap_t - swap_f} Mo sur {swap_t})",
        ))
    return rows


def check_updates() -> tuple[str, bool, bool, str]:
    try:
        out = subprocess.run(
            ["apt", "list", "--upgradable"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ, "LC_ALL": "C"},
        ).stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ("Mises à jour", False, False, f"indéterminable ({exc})")
    count = sum(1 for l in out.splitlines() if "/" in l and "Listing" not in l)
    # les mises à jour de sécurité sont prioritaires
    secu = sum(1 for l in out.splitlines() if "security" in l.lower())
    detail = f"{count} en attente"
    if secu:
        detail += f", dont {secu} de sécurité"
    return ("Mises à jour", count < UPDATES_WARN and secu == 0, False, detail)


def check_radius() -> tuple[str, bool, bool, str]:
    try:
        out = subprocess.run(
            ["ss", "-lun"], capture_output=True, text=True, timeout=20
        ).stdout
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ("RADIUS", False, False, f"indéterminable ({exc})")
    has1812 = bool(re.search(r":1812\b", out))
    has1813 = bool(re.search(r":1813\b", out))
    if has1812 and has1813:
        return ("RADIUS", True, False, "ports 1812 et 1813 en écoute")
    manquants = ", ".join(p for p, ok in (("1812", has1812), ("1813", has1813)) if not ok)
    return ("RADIUS", False, True, f"port(s) absent(s) : {manquants}")


def check_portal() -> tuple[str, bool, bool, str]:
    req = urllib.request.Request(PORTAL_URL, headers={"User-Agent": "WaveFi-VPS-Check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            code = resp.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except Exception as exc:  # noqa: BLE001 — on veut tout remonter
        return ("Portail", False, True, f"injoignable ({exc})")
    return ("Portail", code == 200, code != 200, f"HTTP {code}")


# --- envoi ------------------------------------------------------------------
def load_webhook() -> str:
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith(("DISCORD_WEBHOOK=", "DISCORD_WEBHOOK_URL=")):
                return line.split("=", 1)[1].strip()
    return (os.environ.get("DISCORD_WEBHOOK") or os.environ.get("DISCORD_WEBHOOK_URL") or "").strip()


def send_discord(webhook: str, content: str, timeout: float = 20.0) -> bool:
    payload = json.dumps({"content": content[:1900]}).encode("utf-8")
    req = urllib.request.Request(
        webhook, data=payload, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "WaveFi-VPS-Check/1.0"},
    )
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return 200 <= resp.status < 300
        except Exception:  # noqa: BLE001
            if attempt == 2:
                return False
            time.sleep(3)
    return False


# --- principal --------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Contrôle de santé du VPS WaveFi.")
    parser.add_argument("--dry-run", action="store_true", help="affiche sans envoyer")
    parser.add_argument("--heartbeat", action="store_true",
                        help="envoie le rapport même si tout va bien")
    args = parser.parse_args(argv)

    rows: list[tuple[str, bool, bool, str]] = [
        check_disk(),
        *check_memory(),
        check_updates(),
        check_radius(),
        check_portal(),
    ]

    problems = [r for r in rows if not r[1]]
    critical = [r for r in rows if r[2]]

    lines = [f"**VPS WaveFi — {now_label()}**"]
    for name, ok, crit, detail in rows:
        icon = "✅" if ok else ("🚨" if crit else "⚠️")
        lines.append(f"{icon} {name} : {detail}")

    if problems:
        header = "🚨 **ALERTE VPS**" if critical else "⚠️ **VPS — à surveiller**"
        lines.insert(0, header)
    elif args.heartbeat:
        lines.insert(0, "💚 **VPS — tout va bien**")
    message = "\n".join(lines)

    print(message, flush=True)
    for name, ok, _, detail in rows:
        print(f"[{name}] {'OK' if ok else 'ALERTE'} — {detail}", file=sys.stderr, flush=True)

    if args.dry_run:
        return 1 if problems else 0

    if not problems and not args.heartbeat:
        return 0  # silence volontaire

    webhook = load_webhook()
    if not webhook:
        print("Discord : webhook introuvable (~/.wavefi.env).", file=sys.stderr)
        return 2
    if not send_discord(webhook, message):
        print("Discord : échec de l'envoi.", file=sys.stderr)
        return 2
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"Erreur d'exécution : {exc}", file=sys.stderr)
        sys.exit(3)
