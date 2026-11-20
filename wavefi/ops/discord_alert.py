#!/usr/bin/env python3
"""Envoie une alerte vers un webhook Discord.

Usage :
    python3 ops/discord_alert.py "Sauvegarde terminée"
    echo "Disque à 92 %" | python3 ops/discord_alert.py

L'URL du webhook est lue dans cet ordre :
  1. option --webhook
  2. variable d'environnement DISCORD_WEBHOOK_URL
  3. fichier de configuration (ops/discord.env par défaut)

Le script ne dépend que de la bibliothèque standard (Python 3.9+).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MAX_CONTENT = 2000
DEFAULT_TIMEOUT = 10.0
DEFAULT_USERNAME = "WaveFi Alertes"
CONFIG_FILENAME = "discord.env"

DISCORD_HOSTS = frozenset(
    {
        "discord.com",
        "discordapp.com",
        "ptb.discord.com",
        "canary.discord.com",
    }
)

# Marqueurs d'une URL encore laissée à l'état d'exemple.
PLACEHOLDER_TOKENS = ("colle", "votre_url", "exemple")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CONFIG = 2
EXIT_HTTP = 3
EXIT_NETWORK = 4


class AlertError(Exception):
    """Erreur attendue, associée à un code de sortie."""

    exit_code = EXIT_USAGE


class ConfigError(AlertError):
    """Configuration absente ou invalide."""

    exit_code = EXIT_CONFIG


class WebhookError(AlertError):
    """Discord a refusé la requête."""

    exit_code = EXIT_HTTP


class NetworkError(AlertError):
    """Le webhook est injoignable."""

    exit_code = EXIT_NETWORK


def default_config_path() -> Path:
    """Emplacement par défaut du fichier contenant l'URL du webhook."""
    return Path(__file__).resolve().parent / CONFIG_FILENAME


def resolve_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    from_env = os.environ.get("DISCORD_ALERT_CONFIG")
    if from_env:
        return Path(from_env).expanduser()
    return default_config_path()


def read_config(path: Path) -> dict[str, str]:
    """Lit un fichier KEY=VALUE simple (commentaires avec #)."""
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise ConfigError(
            f"Lecture impossible du fichier de configuration {path} : "
            f"{exc.strerror or exc}"
        ) from exc

    values: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if key:
            values[key] = value.strip().strip("'\"")
    return values


def resolve_settings(args: argparse.Namespace) -> tuple[str, str]:
    """Résout l'URL et le nom d'affichage (CLI > env > fichier)."""
    webhook = (args.webhook or os.environ.get("DISCORD_WEBHOOK_URL") or "").strip()
    username = (args.username or os.environ.get("DISCORD_ALERT_USERNAME") or "").strip()

    path = resolve_config_path(args.config)
    if path.is_file():
        values = read_config(path)
        webhook = webhook or values.get("DISCORD_WEBHOOK_URL", "").strip()
        username = username or values.get("DISCORD_ALERT_USERNAME", "").strip()
    elif args.config:
        raise ConfigError(f"Fichier de configuration introuvable : {path}")

    return webhook, username or DEFAULT_USERNAME


def validate_webhook(url: str) -> str:
    """Refuse tout ce qui n'est pas un webhook Discord en HTTPS."""
    url = url.strip()
    if not url:
        raise ConfigError(
            "Aucune URL de webhook configurée. Renseignez DISCORD_WEBHOOK_URL "
            f"dans {default_config_path()}, ou exportez cette variable "
            "d'environnement."
        )

    lowered = url.lower()
    if any(token in lowered for token in PLACEHOLDER_TOKENS):
        raise ConfigError(
            "L'URL du webhook est encore un exemple : remplacez-la par la vraie "
            "URL fournie par Discord."
        )

    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https":
        raise ConfigError("L'URL du webhook doit commencer par https://")
    if parsed.hostname not in DISCORD_HOSTS:
        raise ConfigError(
            f"Hôte non autorisé ({parsed.hostname!r}) : utilisez une URL "
            "discord.com/api/webhooks/..."
        )
    if not parsed.path.startswith("/api/webhooks/"):
        raise ConfigError(
            "Le chemin de l'URL doit être /api/webhooks/<id>/<token>."
        )

    segments = [segment for segment in parsed.path.split("/") if segment]
    if len(segments) < 4:
        raise ConfigError(
            "URL de webhook incomplète : /api/webhooks/<id>/<token> attendu."
        )

    return url


def build_payload(message: str, username: str) -> dict[str, object]:
    content = message.strip()
    if not content:
        raise AlertError(
            "Le message est vide. Exemple : "
            'python3 ops/discord_alert.py "Sauvegarde terminée"'
        )

    if len(content) > MAX_CONTENT:
        marker = "\n… [tronqué]"
        content = content[: MAX_CONTENT - len(marker)] + marker
        print("Attention : message tronqué à 2 000 caractères.", file=sys.stderr)

    return {
        "content": content,
        "username": username,
        # Aucune notification de masse : un message d'alerte ne doit pas
        # pouvoir déclencher @everyone ou @here.
        "allowed_mentions": {"parse": []},
    }


def _retry_delay(exc: urllib.error.HTTPError, attempt: int) -> float:
    header = exc.headers.get("Retry-After") if exc.headers else None
    if header:
        try:
            return min(max(float(header), 0.0), 10.0)
        except ValueError:
            pass
    return min(2 ** (attempt - 1), 5.0)


def send(
    webhook: str,
    payload: dict[str, object],
    timeout: float = DEFAULT_TIMEOUT,
    attempts: int = 3,
) -> None:
    """POST le payload sur le webhook, avec reprise sur 429/5xx/réseau."""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "wavefi-discord-alert/1.0",
    }

    last_error: AlertError | None = None
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(
            webhook, data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                response.read()
                if 200 <= response.status < 300:
                    return
                last_error = WebhookError(
                    f"Discord a répondu HTTP {response.status}."
                )
                if attempt == attempts:
                    raise last_error
            time.sleep(min(2 ** (attempt - 1), 5.0))
        except urllib.error.HTTPError as exc:
            detail = exc.read(400).decode("utf-8", "replace").strip()
            retryable = exc.code == 429 or 500 <= exc.code < 600
            message = f"Discord a répondu HTTP {exc.code}"
            if detail:
                message += f" : {detail}"
            last_error = WebhookError(message)
            if not retryable or attempt == attempts:
                raise last_error from None
            time.sleep(_retry_delay(exc, attempt))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            last_error = NetworkError(f"Connexion au webhook impossible : {reason}")
            if attempt == attempts:
                raise last_error from None
            time.sleep(min(2 ** (attempt - 1), 5.0))

    raise last_error or AlertError("Échec de l'envoi de l'alerte.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Envoie un message sur un webhook Discord.",
        epilog=(
            "URL lue depuis --webhook, DISCORD_WEBHOOK_URL, puis ops/discord.env."
        ),
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message à envoyer (sinon lu sur l'entrée standard).",
    )
    parser.add_argument("--webhook", help="URL du webhook Discord (prioritaire).")
    parser.add_argument("--username", help="Nom affiché de l'alerte.")
    parser.add_argument(
        "--config",
        help="Fichier de configuration (défaut : ops/discord.env).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Délai d'expiration en secondes (défaut : {DEFAULT_TIMEOUT:g}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valide la configuration et affiche la requête sans l'envoyer.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="N'affiche rien en cas de succès.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.message:
            message = " ".join(args.message)
        elif not sys.stdin.isatty():
            message = sys.stdin.read()
        else:
            raise AlertError(
                "Aucun message fourni. Exemple : "
                'python3 ops/discord_alert.py "Sauvegarde terminée"'
            )

        if args.timeout <= 0:
            raise AlertError("--timeout doit être strictement positif.")

        webhook, username = resolve_settings(args)
        webhook = validate_webhook(webhook)
        payload = build_payload(message, username)

        if args.dry_run:
            print(f"Cible : {urllib.parse.urlsplit(webhook).hostname}")
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            print("Mode --dry-run : rien n'a été envoyé.")
            return EXIT_OK

        send(webhook, payload, timeout=args.timeout)
        if not args.quiet:
            print("Alerte Discord envoyée.")
        return EXIT_OK

    except AlertError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return exc.exit_code
    except KeyboardInterrupt:
        print("Interrompu.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
