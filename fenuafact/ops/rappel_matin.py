#!/usr/bin/env python3
"""Envoie un rappel sur Discord. Utilisé par une tâche one-shot `at`.

Usage :
    python3 rappel_matin.py "message"
    python3 rappel_matin.py --file message.txt

Le webhook est lu dans DISCORD_WEBHOOK_URL (env) ou ops/discord.env.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENV = HERE / "discord.env"
LOG = HERE / "rappel.log"
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


def main() -> int:
    load_env(ENV)

    if len(sys.argv) < 2:
        print("message manquant", file=sys.stderr)
        return 2

    if sys.argv[1] == "--file":
        message = Path(sys.argv[2]).read_text(encoding="utf-8")
    else:
        message = " ".join(sys.argv[1:])

    webhook = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        print("DISCORD_WEBHOOK_URL absente", file=sys.stderr)
        return 1

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
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(f"envoyé ({len(message)} caractères)\n")
        print("rappel envoyé")
        return 0
    except Exception as exc:
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(f"ÉCHEC : {exc}\n")
        print(f"ÉCHEC : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
