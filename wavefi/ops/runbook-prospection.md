# Runbook — pipeline de prospection WaveFi

**Périmètre :** tunnel `prospection_wifi/` (agent local historique), conservé dans
`ops/legacy-agent/`. **Aucun envoi d'e-mail n'est automatisé.** Chaque étape se lance à la main.

> ⚠️ **Règle d'or :** toujours commencer par `--dry-run` et `--limit`, puis relancer sans limite
> seulement après vérification. Les étapes 1 à 8 consomment des API payantes (Apify, TypeSafe,
> Hunter.io, Brevo, DeepSeek).

---

## 1. Préparation

```bash
cd /root/workspace/projets-clients/wavefi/ops/legacy-agent

# Environnement Python dédié (une seule fois)
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt        # pipeline + Playwright (export PDF)
pip install pytest rich                # tests hors ligne + rendu console

# Navigateur pour l'export PDF (une seule fois, ~230 Mo)
playwright install chromium
```

Configuration des clés :

```bash
cd prospection_wifi
cp env.example.txt .env
chmod 600 .env
# éditer .env : APIFY_API_KEY, TYPESAFE_API_KEY, DEEPSEEK_API_KEY,
#               HUNTER_API_KEY, BREVO_API_KEY, FACEBOOK_API_KEY (facultatif)
```

Le fichier `.env` est ignoré par Git. Ne jamais le copier dans un document ni dans un CSV.

## 2. Déroulé du pipeline

Toutes les commandes se lancent depuis `prospection_wifi/` et écrivent leurs CSV dans ce dossier.

| # | Commande | Entrée → sortie | Coût |
|---|---|---|---|
| 1 | `python3 scraper.py --limit 10 --dry-run` puis `python3 scraper.py --limit 10` | Apify → `leads_polynesie.csv` | Apify |
| 2 | `python3 clean_leads.py --dry-run` puis `python3 clean_leads.py` | `leads_polynesie.csv` → `leads_polynesie_filtres.csv` | gratuit |
| 3 | `python3 scorer.py --input leads_polynesie_filtres.csv --limit 10 --dry-run` puis `python3 scorer.py --input leads_polynesie_filtres.csv` | `leads_polynesie_filtres.csv` → `leads_scores.csv` | TypeSafe |
| 4 | `python3 emailer.py --limit 5 --dry-run` puis `python3 emailer.py --limit 5` | `leads_scores.csv` → `campagne_wifi_polynesie.csv`, `campagne_wifi_master.csv` | DeepSeek |
| 5 | `python3 enricher.py --limit 5` | `campagne_wifi_polynesie.csv` → `campagne_wifi_enrichie.csv` | gratuit |
| 6 | `python3 enricher_hunter.py --limit 5 --dry-run` puis `python3 enricher_hunter.py --limit 5` | `campagne_wifi_enrichie.csv` → `campagne_wifi_final.csv` | Hunter.io |
| 7 | `python3 enricher_netanalyzer.py --dry-run` puis `python3 enricher_netanalyzer.py` | `campagne_wifi_final.csv` + `donnees_wifi_netanalyzer.csv` → `campagne_wifi_ultime.csv` | gratuit |
| 8 | `python3 enricher_facebook.py --limit 3 --dry-run` puis `python3 enricher_facebook.py --limit 3` | `campagne_wifi_ultime.csv` → `campagne_wifi_facebook.csv` | Apify |
| 9 | `python3 fusionner_emails.py --dry-run` puis `python3 fusionner_emails.py` | tous les CSV d'e-mails → `leads_enrichis_globaux.csv` | gratuit |
| 10 | `python3 generer_campagne_terrain.py --dry-run` puis `python3 generer_campagne_terrain.py` | scans + campagne → `campagne_terrain.csv` | gratuit |
| 11 | `python3 enrichir_adresses_terrain.py --limite 5 --dry-run` puis `python3 enrichir_adresses_terrain.py` | `campagne_terrain.csv` → `campagne_terrain_adresses.csv` | Apify |
| 12 | `python3 dashboard.py` | `leads_scores.csv` → `leads_scores.html` | gratuit |
| 13 | `python3 ../../notify-prospection.py --dry-run` puis `python3 ../../notify-prospection.py` | `campagne_wifi_master.csv` → message Discord | gratuit |

**Étape 4 sans rappeler l'API :** `python3 emailer.py --assemble` reconstruit
`campagne_wifi_master.csv` à partir des textes déjà générés (aucun appel DeepSeek).

**Étape 13 :** le message Discord ne contient que des compteurs (leads, e-mails disponibles,
envois journalisés), jamais de nom ni d'adresse. Il utilise `ops/discord.env` et
`ops/discord_alert.py`.

## 3. Envoi des e-mails — manuel, jamais automatique

```bash
cd /root/workspace/projets-clients/wavefi/ops/legacy-agent/prospection_wifi

python3 sender.py --dry-run                  # 1. aperçu, aucun appel Brevo
python3 sender.py --limit 1 --dry-run        # 2. vérifier un destinataire précis
python3 sender.py --limit 1                  # 3. test réel, un seul lead
python3 sender.py --business-hours \
  --sent-log envois.csv                      # 4. campagne (mardi-jeudi, 8h-10h / 13h-15h)
```

- `--sent-log` empêche les doublons ; `--force` réenvoie malgré tout (à éviter).
- Seul `email_1` part : les relances (`email_2`, `email_3`) restent manuelles.
- **Ne jamais** brancher `sender.py` sur un cron, un webhook ou une boucle automatique.
- Avant un envoi réel : vérifier l'expéditeur validé dans Brevo (`contact@wavefi.tech`), le lien
  de désabonnement `{{ unsubscribe }}` et le registre des oppositions.

## 4. Données et sauvegarde

Les CSV sont **ignorés par Git** mais restent sur le disque (le pipeline en a besoin).

```bash
# Sauvegarde datée des données de campagne
cd /root/workspace/projets-clients/wavefi
tar czf Archives/prospection-donnees-$(date +%F).tar.gz \
  ops/legacy-agent/prospection_wifi/*.csv
```

Après une campagne, copier les fichiers de référence dans
`03_Commercial_et_Prospection/1_Tableaux_Suivi/Donnees_Leads/` (source de vérité documentaire),
puis laisser le reste en `Archives/`.

## 5. Purge de l'historique Git — **à ne pas exécuter maintenant**

L'historique du dépôt distant contient encore les CSV de leads et le code de l'agent. Les
commandes ci-dessous sont préparées pour plus tard, **après sauvegarde et validation**.

```bash
# 1. Sauvegarde complète (miroir + bundle) — OBLIGATOIRE avant toute réécriture
#    (dépôt privé : authentification GitHub requise)
cd /root
git clone --mirror https://github.com/trebron77/wavefi-prospection.git \
  wavefi-prospection-backup.git
cd wavefi-prospection-backup.git
git bundle create ../wavefi-prospection-$(date +%F).bundle --all

# 2. Réécriture de l'historique (git-filter-repo à installer : pip install git-filter-repo)
rm -rf /tmp/wavefi-prospection-clean
git clone https://github.com/trebron77/wavefi-prospection.git /tmp/wavefi-prospection-clean
cd /tmp/wavefi-prospection-clean
git filter-repo --path-glob 'prospection_wifi/*.csv' --path app.py --path src/ --invert-paths
git remote add origin https://github.com/trebron77/wavefi-prospection.git

# 3. Vérification avant diffusion
git log --oneline --all | head
git ls-files | grep -c '\.csv$'        # doit afficher 0
git log --all -- prospection_wifi | head

# 4. Publication (irréversible côté distant)
git push --force --all
git push --force --tags
```

Après la purge : prévenir les collaborateurs de re-cloner, supprimer les anciens clones locaux, et
vérifier que GitHub n'a pas conservé de copie (forks, caches, PR). Tant que cette section n'a pas
été exécutée, l'historique reste intact — c'est volontaire.

## 6. Dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `Clé APIFY_API_KEY manquante` | `.env` absent ou incomplet | Copier `env.example.txt` vers `.env`, renseigner la clé |
| `401` sur DeepSeek | clé révoquée ou mauvais endpoint | Vérifier `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL` |
| `400` Brevo | expéditeur non validé | Valider `contact@wavefi.tech` dans Brevo |
| `ModuleNotFoundError: pandas` | venv incomplet | `pip install -r requirements.txt` |
| PDF impossible | Chromium absent | `playwright install chromium` |
| `git pull` échoue | clone local modifié (agent archivé, CSV ignorés) | Ne pas forcer ; récupérer les fichiers utiles à la main |

## 7. Tests hors ligne

```bash
cd /root/workspace/projets-clients/wavefi/ops/legacy-agent
.venv/bin/python -m pytest -q
```

Résultat attendu : **331 passed** (aucun réseau, aucun fichier du projet modifié).
`rich` est nécessaire pour le test du rendu console ; sans lui, un test est ignoré.

Validation du 2026-11-14 : Python 3.14.4, pandas 3.1.1, pytest 9.2.0.

## 8. État local du dépôt

- L'agent (`src/`, `app.py`, tests associés) est archivé dans `Archives/legacy-agent/`.
- Les CSV sont retirés du suivi Git et ajoutés au `.gitignore`.
- Les modifications locales ne sont **pas poussées** ; elles servent à figer l'état de travail.
