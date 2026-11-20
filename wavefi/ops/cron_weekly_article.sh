#!/usr/bin/env bash
# Génère automatiquement l'article SEO hebdomadaire de WaveFi.
#
# Déroulé :
#   1. choisit un sujet non encore traité parmi les sujets prioritaires ;
#   2. si la liste prioritaire est épuisée, pioche dans une liste de secours ;
#   3. si tout est fait, crée un nouveau sujet à partir d'une matrice
#      secteur × localité, toujours sans doublon ;
#   4. appelle ops/generate_article.py, qui écrit l'article dans content/
#      et envoie l'alerte Discord.
#
# Usage :
#   ops/cron_weekly_article.sh
#   ops/cron_weekly_article.sh --dry-run   # affiche le sujet choisi, sans générer
#   ops/cron_weekly_article.sh --help
#
# La variable WAVEFI_CONTENT_DIR permet de tester la sélection sur un dossier
# factice ; elle n'est pas utilisée en production.

set -euo pipefail

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# readlink -f résout un éventuel appel via le lien symbolique workspace/ops,
# pour que content/ et ops/ restent ceux du projet réel.
SELF="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT="$(cd "$(dirname "$SELF")/.." && pwd -P)"
cd "$ROOT"

PYTHON="${PYTHON:-$(command -v python3)}"
GENERATOR="$ROOT/ops/generate_article.py"
ALERT="$ROOT/ops/discord_alert.py"

DRY_RUN=0
case "${1:-}" in
    --dry-run)
        DRY_RUN=1
        ;;
    --help | -h)
        sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
        exit 0
        ;;
    "")
        ;;
    *)
        echo "Option inconnue : $1" >&2
        exit 1
        ;;
esac

# Sélection du sujet. Le code Python réutilise le slugify du générateur pour
# vérifier l'existence d'un article sans dupliquer la logique d'accents.
set +e
SELECTION="$("$PYTHON" - "$ROOT" <<'PY'
import os
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])
content_dir = Path(os.environ.get("WAVEFI_CONTENT_DIR") or (root / "content"))
sys.path.insert(0, str(root / "ops"))
from generate_article import slugify

# Sujets prioritaires : les 5 demandés + le transport de passagers inter-îles.
PRIMARY = [
    "Le Wi-Fi marketing pour les opticiens",
    "Le Wi-Fi marketing pour les cabinets dentaires",
    "Le Wi-Fi marketing pour les concessions automobiles",
    "Le Wi-Fi marketing pour les magasins de perles",
    "Le Wi-Fi marketing pour les agences de location de voiture",
    "Le Wi-Fi marketing pour les compagnies de transport inter-îles en Polynésie",
]

# Briefs spécifiques : ils nomment les cibles sans affirmer de faits sur elles.
BRIEFS = {
    "Le Wi-Fi marketing pour les compagnies de transport inter-îles en Polynésie": (
        "Cible : directions d'Aremiti, Apetahi Express, Aranui, Dory2 et des "
        "autres compagnies de transport de passagers inter-îles en Polynésie. "
        "Angle : l'accueil et l'information des passagers avant l'embarquement "
        "(files, attente, formalités), la continuité de service pendant la "
        "traversée, et des offres ciblées pour les excursions et les partenaires "
        "locaux. Mentionne les archipels éloignés (Marquises, Tuamotu, Gambier, "
        "Australes) lorsque c'est pertinent. Ne fais aucune affirmation sur les "
        "flottes, équipements, horaires ou politiques de ces compagnies : ce sont "
        "des exemples de cible, pas des sources. Aucun chiffre, aucune "
        "statistique, aucun tarif inventé."
    ),
}

# Nouveaux sujets ajoutés une fois les sujets prioritaires traités.
FALLBACK = [
    "Le Wi-Fi marketing pour les pharmacies",
    "Le Wi-Fi marketing pour les boulangeries et pâtisseries",
    "Le Wi-Fi marketing pour les agences de voyage",
    "Le Wi-Fi marketing pour les loueurs de scooters",
    "Le Wi-Fi marketing pour les spas et centres de bien-être",
    "Le Wi-Fi marketing pour les écoles de surf",
    "Le Wi-Fi marketing pour les roulottes et snack-bars",
    "Le Wi-Fi marketing pour les marinas",
    "Le Wi-Fi marketing pour les jardineries",
    "Le Wi-Fi marketing pour les salles de spectacle",
]

# Dernier recours : de nouvelles combinaisons secteur × localité, pour que le
# cron continue à produire des sujets inédits même après plusieurs mois.
SECTORS = [
    "les cabinets vétérinaires",
    "les auto-écoles",
    "les clubs de plongée",
    "les loueurs de bateaux",
    "les entreprises du bâtiment",
    "les agences de communication",
    "les crèches privées",
    "les magasins de sport",
    "les restaurants de bord de mer",
    "les guinguettes",
]
LOCALITIES = [
    "Papeete",
    "Pirae",
    "Arue",
    "Mahina",
    "Faa'a",
    "Punaauia",
    "Paea",
    "Papara",
    "Moorea",
    "Bora Bora",
]
MATRIX = [
    f"Le Wi-Fi marketing pour {sector} à {locality}"
    for sector in SECTORS
    for locality in LOCALITIES
]


def article_exists(topic: str) -> bool:
    filename = f"article-{slugify(topic)}.md"
    return (content_dir / filename).is_file()


def pick_available(topics: list[str]) -> str | None:
    available = [topic for topic in topics if not article_exists(topic)]
    return random.choice(available) if available else None


for group in (PRIMARY, FALLBACK, MATRIX):
    chosen = pick_available(group)
    if chosen:
        print(f"{chosen}\t{BRIEFS.get(chosen, '')}")
        break
else:
    sys.exit(3)
PY
)"
STATUS=$?
set -e

if ((STATUS != 0)); then
    if ((STATUS == 3)); then
        MESSAGE="❌ Stock de sujets épuisé : aucun article hebdomadaire généré."
    else
        MESSAGE="❌ Sélection du sujet impossible (code ${STATUS}) : aucun article généré."
    fi
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] ${MESSAGE}" >&2
    "$PYTHON" "$ALERT" "$MESSAGE" || true
    exit "$STATUS"
fi

TOPIC="${SELECTION%%$'\t'*}"
BRIEF=""
if [[ "$SELECTION" == *$'\t'* ]]; then
    BRIEF="${SELECTION#*$'\t'}"
fi

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Sujet choisi : ${TOPIC}"
if [[ -n "$BRIEF" ]]; then
    echo "Brief : ${BRIEF}"
fi

if ((DRY_RUN)); then
    echo "Mode --dry-run : aucun article généré."
    exit 0
fi

GENERATOR_ARGS=("$TOPIC")
if [[ -n "$BRIEF" ]]; then
    GENERATOR_ARGS=(--brief "$BRIEF" "$TOPIC")
fi

if "$PYTHON" "$GENERATOR" "${GENERATOR_ARGS[@]}"; then
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Génération terminée : ${TOPIC}"
else
    STATUS=$?
    echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Échec de la génération (code ${STATUS}) : ${TOPIC}" >&2
    "$PYTHON" "$ALERT" "❌ Échec de la génération hebdomadaire : ${TOPIC}" || true
    exit "$STATUS"
fi
