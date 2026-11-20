# Legacy agent — archive

Code de l'**agent de développement autonome local** extrait du dépôt `trebron77/wavefi-prospection`
(anciennement `local-dev-agent-01`), archivé le **2026-11-14**.

## Pourquoi cet archivage

Cet agent (boucle « raisonner → agir → observer », outils fichiers/recherche/shell/git, interface
Streamlit) refaisait ce que Hotumana assure déjà dans cet espace de travail, avec un second accès
shell et ses propres garde-fous. Il n'est **pas exécuté** ici. Le code est conservé pour référence
et pour un usage éventuel sur un poste Windows, où il a été développé.

Le tunnel de prospection (`prospection_wifi/`) reste, lui, actif dans `ops/legacy-agent/`.

## Contenu

| Élément | Rôle d'origine |
|---|---|
| `app.py` | Interface Streamlit de chat, lancée avec `--yes` (approbation automatique des commandes shell). |
| `src/agent.py` | Boucle agentique, journal JSONL, CLI. |
| `src/ui.py` | Session interactive multi-tours (`rich`). |
| `src/llm_client.py` | Client compatible OpenAI (texte, tool_calls, streaming, erreurs). |
| `src/context.py` | Budget de contexte et instantané du projet. |
| `src/tools/` | Cinq outils bornés : fichiers, recherche, shell, git. |
| `tests/` | Tests de l'agent (dont `conftest.py` et `helpers.py`). |

## Provenance

- Dépôt : `github.com/trebron77/wavefi-prospection` (privé)
- Commit : `83649d6` — 2026-11-05
- Emplacement d'origine : `ops/legacy-agent/`

## Remettre en service (si nécessaire)

L'archive n'est pas un projet autonome : elle attend le reste du dépôt (`.env.example`,
`requirements.txt`, `pyproject.toml`).

```bash
cd projets-clients/wavefi
cp -r Archives/legacy-agent/src Archives/legacy-agent/app.py ops/legacy-agent/
cp Archives/legacy-agent/tests/*.py ops/legacy-agent/tests/
cd ops/legacy-agent
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m pytest          # doit passer hors ligne
python src/agent.py --dry-run
```

> ⚠️ `app.py` approuve d'avance les commandes sensibles (`--yes`). Ne jamais l'exposer sur un
> serveur public ; l'utiliser uniquement en local.
