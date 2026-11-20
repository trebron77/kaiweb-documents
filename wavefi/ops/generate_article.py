#!/usr/bin/env python3
"""Génère un article de blog SEO avec l'API DeepSeek, puis alerte Discord.

Usage :
    python3 ops/generate_article.py "Le Wi-Fi dans les salons de coiffure"
    python3 ops/generate_article.py --brief "Cible : ... Angle : ..." "Sujet"
    python3 ops/generate_article.py --force "Sujet déjà traité"
    python3 ops/generate_article.py --dry-run "Sujet"   # affiche les prompts

L'article est enregistré dans content/article-<slug>.md, puis
ops/discord_alert.py est appelé avec le nom du fichier créé.

Configuration (dans l'ordre : CLI > environnement > fichier) :
  - clé API       : --api-key, DEEPSEEK_API_KEY, ops/deepseek.env
  - URL de base   : DEEPSEEK_BASE_URL (défaut : https://api.deepseek.com)
  - modèle        : --model, DEEPSEEK_MODEL (défaut : deepseek-flash)

La bibliothèque openai est cherchée dans l'interpréteur courant, puis dans
ops/.venv : le script se relance automatiquement avec ce venv si besoin.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OPS_DIR = BASE_DIR / "ops"
CONTENT_DIR = BASE_DIR / "content"
ALERT_SCRIPT = OPS_DIR / "discord_alert.py"
DEFAULT_CONFIG = OPS_DIR / "deepseek.env"
VENV_PYTHON = OPS_DIR / ".venv" / "bin" / "python"

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-flash"
DEFAULT_TIMEOUT = 180.0
DEFAULT_MAX_TOKENS = 8192

# Bornes de qualité : en dehors, on demande une réécriture à l'API.
MIN_WORDS = 800
MAX_WORDS = 1350
TARGET_MIN_WORDS = 950
TARGET_MAX_WORDS = 1150

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CONFIG = 2
EXIT_API = 3
EXIT_FILE = 4
EXIT_QUALITY = 5
EXIT_ALERT = 6


SYSTEM_PROMPT = """Tu es rédacteur SEO senior francophone pour WaveFi, solution de Wi-Fi marketing validée par la DGEN (Direction générale de l'économie numérique) en Polynésie française.

MISSION
Rédiger un article de blog SEO complet et prêt à publier pour des décideurs locaux en Polynésie française — dirigeants de commerces et de PME, responsables d'équipements et d'infrastructures (aéroports, ports, terminaux) — sans te limiter à une seule zone.

PUBLIC ET TON
- Cible : décideurs et directions locales (le brief précise le secteur et le niveau de décision).
- Ton : professionnel, direct, concret, chaleureux, ancré dans le contexte polynésien. Pas de jargon marketing creux, pas de superlatifs, pas de condescendance.
- Français soigné, phrases courtes, paragraphes de 2 à 4 phrases.
- Ancre localement le propos sans inventer de faits locaux.

ANCRAGE LOCAL — VARIÉTÉ OBLIGATOIRE
- Pour chaque article, choisis aléatoirement 2 ou 3 localités parmi : Papeete, Pirae, Arue, Mahina, Hitia'a, Taravao, Faa'a, Punaauia, Paea, Papara, Moorea, Bora Bora, Raiatea, Huahine.
- Ne reprends pas systématiquement « Papeete, Faa'a, Punaauia » : cette combinaison ne doit pas être un réflexe. Varie les localités d'un article à l'autre.
- Si le sujet le justifie (tourisme, transport inter-îles, santé, pêche, perliculture, artisanat, etc.), tu peux aussi citer une île des archipels éloignés : Marquises, Tuamotu, Gambier, Australes.
- Chaque localité citée doit être pertinente pour le sujet ; ne juxtapose pas une liste de communes sans lien avec le propos.
- N'invente aucun fait local, aucun équipement, aucune statistique propre à une commune ou à une île.

RÈGLES DE FOND, NON NÉGOCIABLES
1. Validation DGEN : mentionne-la au maximum DEUX fois dans tout l'article (une fois dans le corps, une fois dans la signature finale). Formule-la avec exactitude, sans en faire un slogan ni la répéter dans chaque section.
2. Aucun chiffre inventé : aucune statistique, aucun pourcentage, aucun prix, aucune durée de résultat, aucune promesse chiffrée, aucun témoignage ni nom de client inventé. Si une donnée serait utile, exprime-la qualitativement (« plus vite », « sans changer d'abonnement ») au lieu de la chiffrer.
3. Ne garantis aucun résultat (visibilité, chiffre d'affaires, nombre d'avis). Reste factuel sur ce que permet un portail captif / une solution de Wi-Fi marketing.
4. Analyse de flux et sûreté : ne décris jamais une surveillance individuelle. Parle uniquement de données agrégées et anonymisées, collectées avec consentement, dans un cadre conforme ; la responsabilité de la sûreté reste aux autorités et aux exploitants compétents. Ne présente pas WaveFi comme un système de sécurité ou de vidéosurveillance.
5. CTA final vers Norbert : contact@wavefi.tech.

STRUCTURE OBLIGATOIRE (Markdown)
1. Un seul titre H1 (`# ...`), accrocheur, qui contient le sujet.
2. Une introduction de 2 à 3 paragraphes qui pose le problème local.
3. Des sections H2 (`## ...`), dont au moins deux contiennent des sous-sections H3 (`### ...`).
4. Une section H2 consacrée à l'objection principale de la cible, intitulée explicitement « Objection : ... », qui nomme l'objection et y répond honnêtement.
5. Une section H2 « FAQ » avec EXACTEMENT 3 questions, chacune en H3 (`### ...`), suivie d'une réponse concise.
6. Un CTA final en H2, avec le contact contact@wavefi.tech et le nom Norbert.
7. Une signature finale d'une ligne mentionnant WaveFi et la validation DGEN.

CONTRAINTES DE FORME
- Longueur : environ 1 000 mots (950 à 1 100 mots), hors balises Markdown.
- Markdown pur : pas de bloc de code, pas de commentaire, pas de méta-note, pas de titre répété.
- Deux listes à puces maximum.
- Commence directement par le H1, sans phrase d'introduction avant.
"""


class ArticleError(Exception):
    """Erreur attendue, associée à un code de sortie."""

    exit_code = EXIT_USAGE


class ConfigError(ArticleError):
    exit_code = EXIT_CONFIG


class APIError(ArticleError):
    exit_code = EXIT_API


class FileError(ArticleError):
    exit_code = EXIT_FILE


class QualityError(ArticleError):
    exit_code = EXIT_QUALITY


class AlertError(ArticleError):
    exit_code = EXIT_ALERT


@dataclass
class Settings:
    api_key: str
    base_url: str
    model: str
    timeout: float
    max_tokens: int


def load_openai():
    """Importe openai, en se relançant dans ops/.venv si nécessaire."""
    try:
        from openai import OpenAI

        return OpenAI
    except ModuleNotFoundError as exc:
        if VENV_PYTHON.is_file() and os.environ.get("WAVEFI_VENV_REEXEC") != "1":
            os.environ["WAVEFI_VENV_REEXEC"] = "1"
            os.execv(
                str(VENV_PYTHON),
                [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]],
            )
        raise ConfigError(
            "La bibliothèque openai est introuvable. Installez-la avec : "
            f"{VENV_PYTHON.parent.parent}/bin/python -m pip install openai "
            "(ou créez ops/.venv)."
        ) from exc


def slugify(text: str, max_length: int = 80) -> str:
    """Transforme un sujet en slug ASCII pour le nom de fichier."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in normalized if not unicodedata.combining(c))
    ascii_text = ascii_text.lower().replace("'", "-").replace("’", "-")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rsplit("-", 1)[0].strip("-")
    return slug


def resolve_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser()
    from_env = os.environ.get("DEEPSEEK_CONFIG")
    if from_env:
        return Path(from_env).expanduser()
    return DEFAULT_CONFIG


def read_env_file(path: Path) -> dict[str, str]:
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


def resolve_settings(args: argparse.Namespace) -> Settings:
    path = resolve_config_path(args.config)
    file_values: dict[str, str] = {}
    if path.is_file():
        file_values = read_env_file(path)
    elif args.config:
        raise ConfigError(f"Fichier de configuration introuvable : {path}")

    api_key = (
        args.api_key
        or os.environ.get("DEEPSEEK_API_KEY")
        or file_values.get("DEEPSEEK_API_KEY", "")
    ).strip()
    if not api_key:
        raise ConfigError(
            "Aucune clé API DeepSeek configurée. Renseignez DEEPSEEK_API_KEY "
            f"dans {path} (chmod 600), ou exportez cette variable "
            "d'environnement, ou utilisez --api-key."
        )

    base_url = (
        os.environ.get("DEEPSEEK_BASE_URL")
        or file_values.get("DEEPSEEK_BASE_URL", "")
        or DEFAULT_BASE_URL
    ).strip()
    model = (args.model or os.environ.get("DEEPSEEK_MODEL") or file_values.get(
        "DEEPSEEK_MODEL", ""
    ) or DEFAULT_MODEL).strip()

    if args.timeout <= 0:
        raise ConfigError("--timeout doit être strictement positif.")

    max_tokens = args.max_tokens or int(
        os.environ.get("DEEPSEEK_MAX_TOKENS")
        or file_values.get("DEEPSEEK_MAX_TOKENS", "")
        or DEFAULT_MAX_TOKENS
    )
    if max_tokens <= 0:
        raise ConfigError("--max-tokens doit être strictement positif.")

    return Settings(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=args.timeout,
        max_tokens=max_tokens,
    )


def brief_section(brief: str | None) -> str:
    brief = (brief or "").strip()
    if not brief:
        return ""
    return f"\nBrief et angle imposés (à respecter scrupuleusement) :\n{brief}\n"


def build_user_prompt(subject: str, brief: str | None = None) -> str:
    return (
        f"Sujet de l'article : {subject}\n"
        f"{brief_section(brief)}\n"
        "Rédige l'article complet en respectant toutes les contraintes. "
        "Commence directement par le H1, sans préambule."
    )


def build_repair_prompt(
    subject: str, brief: str | None, draft: str, problems: list[str]
) -> str:
    details = "\n".join(f"- {problem}" for problem in problems)
    return (
        f"Sujet de l'article : {subject}\n"
        f"{brief_section(brief)}\n"
        "Le brouillon ci-dessous ne respecte pas toutes les contraintes. "
        f"Problèmes détectés :\n{details}\n\n"
        "Réécris l'article COMPLET et corrigé, du H1 à la signature finale, "
        "en conservant ce qui fonctionne. Ne renvoie ni explication ni commentaire.\n\n"
        "--- BROUILLON ---\n"
        f"{draft}"
    )


def clean_markdown(raw: str) -> str:
    """Retire les fences éventuelles et tout préambule avant le H1."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    first_h1 = re.search(r"^#\s+\S", text, re.MULTILINE)
    if first_h1 and first_h1.start() > 0:
        text = text[first_h1.start():]

    return text.rstrip() + "\n"


def count_words(text: str) -> int:
    return len(
        re.findall(
            r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’\-][0-9A-Za-zÀ-ÖØ-öø-ÿ]+)*", text
        )
    )


def count_faq_questions(text: str) -> int:
    in_faq = False
    questions = 0
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.*)$", line)
        if h2:
            title = h2.group(1).strip().lower()
            in_faq = bool(re.search(r"\bfaq\b|foire aux questions", title))
            continue
        if in_faq and re.match(r"^###\s+\S", line):
            questions += 1
    return questions


def validate_article(text: str) -> tuple[list[str], list[str]]:
    """Retourne (erreurs bloquantes, avertissements)."""
    errors: list[str] = []
    warnings: list[str] = []

    h1_count = len(re.findall(r"^#\s+\S", text, re.MULTILINE))
    if h1_count != 1:
        errors.append(f"il faut exactement un H1 (détecté : {h1_count}).")

    h3_count = len(re.findall(r"^###\s+\S", text, re.MULTILINE))
    if h3_count < 3:
        errors.append(f"il faut au moins trois H3 (détecté : {h3_count}).")

    if not re.search(r"^##\s+.*objection", text, re.MULTILINE | re.IGNORECASE):
        errors.append("la section H2 « Objection : ... » est absente.")

    faq_questions = count_faq_questions(text)
    if faq_questions != 3:
        errors.append(f"la FAQ doit contenir exactement 3 questions (détecté : {faq_questions}).")

    dgen_count = len(re.findall(r"\bDGEN\b", text, re.IGNORECASE))
    if dgen_count == 0:
        errors.append("la validation DGEN n'est pas mentionnée.")
    elif dgen_count > 2:
        errors.append(
            f"la DGEN est mentionnée {dgen_count} fois (maximum 2, sans sur-répétition)."
        )

    if "contact@wavefi.tech" not in text.lower():
        errors.append("le CTA final ne contient pas contact@wavefi.tech.")

    words = count_words(text)
    if words < MIN_WORDS or words > MAX_WORDS:
        errors.append(
            f"longueur hors bornes : {words} mots (attendu entre {MIN_WORDS} et {MAX_WORDS})."
        )
    elif words < TARGET_MIN_WORDS or words > TARGET_MAX_WORDS:
        warnings.append(
            f"{words} mots : proche de la cible, mais hors de la plage 950–1 100."
        )

    percentages = re.findall(r"\d+(?:[.,]\d+)?\s*%", text)
    if percentages:
        warnings.append(
            f"{len(percentages)} pourcentage(s) détecté(s) : à relire pour vérifier "
            "qu'aucun chiffre n'est inventé."
        )

    return errors, warnings


def request_article(
    client: object,
    settings: Settings,
    messages: list[dict[str, str]],
) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.model,
            messages=messages,
            temperature=0.7,
            max_tokens=settings.max_tokens,
            stream=False,
        )
    except Exception as exc:  # erreurs SDK, réseau, HTTP, quota…
        raise APIError(f"Appel à l'API DeepSeek impossible : {exc}") from exc

    if not response.choices:
        raise APIError("L'API DeepSeek n'a renvoyé aucune réponse.")

    choice = response.choices[0]
    if choice.finish_reason == "length":
        raise APIError(
            "Réponse tronquée par la limite de tokens : réduisez le sujet ou "
            "augmentez --max-tokens."
        )

    content = (choice.message.content or "").strip()
    if not content:
        raise APIError("L'API DeepSeek a renvoyé un contenu vide.")

    return clean_markdown(content)


def generate_article(
    client: object,
    settings: Settings,
    subject: str,
    *,
    brief: str | None = None,
    allow_retry: bool = True,
) -> tuple[str, list[str]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(subject, brief)},
    ]
    article = request_article(client, settings, messages)

    errors, warnings = validate_article(article)
    if not errors:
        return article, warnings

    if not allow_retry:
        raise QualityError(
            "L'article généré ne respecte pas les contraintes :\n- "
            + "\n- ".join(errors)
        )

    print(
        "Contrôle qualité : réécriture demandée pour corriger "
        f"{len(errors)} point(s).",
        file=sys.stderr,
    )
    repair_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_repair_prompt(subject, brief, article, errors)},
    ]
    repaired = request_article(client, settings, repair_messages)
    errors, warnings = validate_article(repaired)
    if errors:
        raise QualityError(
            "L'article reste non conforme après réécriture :\n- "
            + "\n- ".join(errors)
        )

    return repaired, warnings


def send_alert(filename: str) -> None:
    message = f"✅ Nouvel article généré : {filename}"
    if not ALERT_SCRIPT.is_file():
        raise AlertError(f"Script d'alerte introuvable : {ALERT_SCRIPT}")

    try:
        result = subprocess.run(
            [sys.executable, str(ALERT_SCRIPT), message],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise AlertError(f"Exécution de discord_alert.py impossible : {exc}") from exc

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "aucun détail"
        raise AlertError(
            f"L'alerte Discord a échoué (code {result.returncode}) : {detail}"
        )

    print(message)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Génère un article SEO avec DeepSeek et alerte Discord.",
        epilog=(
            "Clé lue depuis --api-key, DEEPSEEK_API_KEY, puis ops/deepseek.env."
        ),
    )
    parser.add_argument(
        "subject",
        nargs="+",
        help="Sujet de l'article (à mettre entre guillemets).",
    )
    parser.add_argument("--api-key", help="Clé API DeepSeek (prioritaire).")
    parser.add_argument("--model", help=f"Modèle DeepSeek (défaut : {DEFAULT_MODEL}).")
    parser.add_argument(
        "--brief",
        help=(
            "Brief éditorial : cible, angle, points à couvrir, interdits. "
            "Il guide la rédaction mais n'apparaît ni dans le slug ni dans le H1."
        ),
    )
    parser.add_argument(
        "--config",
        help=f"Fichier de configuration (défaut : {DEFAULT_CONFIG.relative_to(BASE_DIR)}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Délai d'expiration de l'API en secondes (défaut : {DEFAULT_TIMEOUT:g}).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help=f"Limite de tokens de la réponse (défaut : {DEFAULT_MAX_TOKENS}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Écrase l'article si le fichier existe déjà.",
    )
    parser.add_argument(
        "--no-retry",
        action="store_true",
        help="N'effectue pas la réécriture automatique en cas de non-conformité.",
    )
    parser.add_argument(
        "--no-alert",
        action="store_true",
        help="N'envoie pas d'alerte Discord.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche les prompts et la cible sans appeler l'API.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        subject = " ".join(args.subject).strip()
        if not subject:
            raise ArticleError("Le sujet est vide.")

        slug = slugify(subject)
        if not slug:
            raise ArticleError(
                "Le sujet ne contient aucun caractère utilisable pour un nom de fichier."
            )

        output_path = CONTENT_DIR / f"article-{slug}.md"
        if output_path.exists() and not args.force:
            raise FileError(
                f"{output_path.relative_to(BASE_DIR)} existe déjà. "
                "Utilisez --force pour l'écraser."
            )

        settings = resolve_settings(args)
        user_prompt = build_user_prompt(subject, args.brief)

        if args.dry_run:
            print(f"Sujet     : {subject}")
            print(f"Fichier   : {output_path.relative_to(BASE_DIR)}")
            print(f"Modèle    : {settings.model}")
            print(f"API       : {settings.base_url}")
            print(f"Alerte    : {'non' if args.no_alert else 'oui'}")
            if args.brief:
                print(f"Brief     : {args.brief}")
            print("\n--- SYSTEM PROMPT ---\n" + SYSTEM_PROMPT)
            print("\n--- USER PROMPT ---\n" + user_prompt)
            print("\nMode --dry-run : aucun appel API, aucun fichier écrit.")
            return EXIT_OK

        OpenAI = load_openai()
        client = OpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
            timeout=settings.timeout,
        )

        print(f"Génération de l'article « {subject} »…", file=sys.stderr)
        article, warnings = generate_article(
            client,
            settings,
            subject,
            brief=args.brief,
            allow_retry=not args.no_retry,
        )

        for warning in warnings:
            print(f"Attention : {warning}", file=sys.stderr)

        try:
            CONTENT_DIR.mkdir(parents=True, exist_ok=True)
            output_path.write_text(article, encoding="utf-8")
        except OSError as exc:
            raise FileError(f"Écriture impossible de {output_path} : {exc}") from exc

        print(
            f"Article enregistré : {output_path.relative_to(BASE_DIR)} "
            f"({count_words(article)} mots)"
        )

        if args.no_alert:
            print("Alerte Discord désactivée (--no-alert).")
        else:
            send_alert(output_path.name)

        return EXIT_OK

    except ArticleError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return exc.exit_code
    except KeyboardInterrupt:
        print("Interrompu.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
