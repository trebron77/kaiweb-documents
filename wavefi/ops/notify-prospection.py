#!/usr/bin/env python3
"""Envoie sur Discord le bilan de fin du pipeline de prospection WaveFi.

Le script ne contacte jamais Brevo et n'envoie aucun e-mail : il lit un CSV de
campagne, compte les leads et leurs adresses, puis transmet un message de
synthèse à ``ops/discord_alert.py``.

Utilisation
-----------
    python3 ops/notify-prospection.py                  # envoi réel
    python3 ops/notify-prospection.py --dry-run        # affiche sans envoyer
    python3 ops/notify-prospection.py --sent-log envois.csv
    python3 ops/notify-prospection.py --input autre_master.csv

Le message ne contient aucune donnée personnelle : uniquement des compteurs.
Codes de sortie : 0 succès, 1 lecture impossible ou envoi en échec.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OPS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = OPS_DIR.parent
DEFAULT_INPUT = PROJECT_DIR / "ops" / "legacy-agent" / "prospection_wifi" / "campagne_wifi_master.csv"
DEFAULT_CONFIG = OPS_DIR / "discord.env"
ALERT_SCRIPT = OPS_DIR / "discord_alert.py"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def read_rows(path: Path) -> list[dict[str, str]]:
    """Lit un CSV en UTF-8 (repli cp1252), avec ou sans BOM."""
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            with open(path, encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle))
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            raise SystemExit(f"Lecture impossible de {path} : {exc.strerror or exc}")
    raise SystemExit(f"Encodage non reconnu pour {path}")


def valid_emails(rows: list[dict[str, str]], column: str = "email_contact") -> set[str]:
    """Ensemble des adresses valides, en minuscules."""
    found = set()
    for row in rows:
        value = (row.get(column) or "").strip().lower()
        if value and EMAIL_RE.match(value):
            found.add(value)
    return found


def build_message(rows: list[dict[str, str]], sent_log: Path | None) -> str:
    """Construit un bilan chiffré, sans donnée personnelle."""
    emails = valid_emails(rows)
    total = len(rows)
    with_email = len(emails)
    without = max(total - with_email, 0)

    lines = [
        f"📊 **Prospection WaveFi** — bilan de fin de pipeline ({datetime.now():%d/%m/%Y %H:%M})",
        f"Leads : {total} · avec e-mail : {with_email} · sans e-mail : {without}",
    ]

    if sent_log:
        envoyes = valid_emails(read_rows(sent_log))
        restants = len(emails - envoyes)
        lines.append(f"Envois journalisés : {len(envoyes)} · restants : {restants}")

    lines.append("Aucun e-mail n'a été envoyé automatiquement.")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bilan Discord de fin de prospection (sans envoi d'e-mails).")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help=f"CSV de campagne (défaut : {DEFAULT_INPUT.name}).")
    parser.add_argument("--sent-log", help="Journal d'envoi Brevo (colonnes de sender.py --sent-log).")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Fichier du webhook Discord.")
    parser.add_argument("--dry-run", action="store_true", help="Affiche le message sans l'envoyer.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_path = Path(args.input).expanduser()
    if not input_path.is_file():
        print(f"CSV introuvable : {input_path}", file=sys.stderr)
        return 1

    sent_log = Path(args.sent_log).expanduser() if args.sent_log else None
    if sent_log and not sent_log.is_file():
        print(f"Journal d'envoi introuvable : {sent_log}", file=sys.stderr)
        return 1

    message = build_message(read_rows(input_path), sent_log)

    if args.dry_run:
        print(message)
        return 0

    command = [
        sys.executable,
        str(ALERT_SCRIPT),
        "--config",
        str(Path(args.config).expanduser()),
        "--username",
        "WaveFi Prospection",
        message,
    ]
    try:
        result = subprocess.run(command, check=False)
    except OSError as exc:
        print(f"Lancement de l'alerte impossible : {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        print("L'alerte Discord a échoué (voir le message ci-dessus).", file=sys.stderr)
        return 1

    print("Bilan de prospection envoyé sur Discord.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
