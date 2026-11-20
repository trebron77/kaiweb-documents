# Audit — agent local historique (`local-dev-agent-01`)

**Date :** 2026-11-14 · **Auteur :** Hotumana · **Périmètre :** dépôt `trebron77/wavefi-prospection` (anciennement `local-dev-agent-01`), cloné dans `ops/legacy-agent/`.

**Commit audité :** `83649d6` — 2026-11-05 — *feat: generation du one-pager ATN au format PDF via Playwright*.

> **Suites :** le dépôt a été passé en privé et le token révoqué le 2026-11-14, après l'audit.
>
> **Point de vigilance immédiat :** au moment de l'audit, l'API GitHub renvoie
> `private: false` / `visibility: public` pour ce dépôt. Il contient 96 leads nominatifs
> (noms, adresses, téléphones, e-mails) et des e-mails de prospection personnalisés.
> Voir §8.1.

---

## 1. Ce qui a été récupéré

| Élément | Valeur |
|---|---|
| Dépôt | `github.com/trebron77/wavefi-prospection` (dépôt `local-dev-agent-01` renommé) |
| Clone | `projets-clients/wavefi/ops/legacy-agent/` |
| Fichiers suivis | 92 (hors `.git`) |
| Taille | 3,8 Mo |
| Code Python | ≈ 18 000 lignes (agent ≈ 5 600, prospection ≈ 12 400, tests ≈ 8 100) |
| Tests | suite `pytest` hors ligne (494 fonctions de test recensées) |
| Données | 17 CSV, 1,2 Mo |
| Secrets | aucun secret trouvé dans les fichiers ni dans l'historique git ; `.env` est ignoré, seul `.env.example` est versionné |

Deux ensembles distincts cohabitent dans le dépôt :

1. **`src/` + `app.py`** — un agent de développement autonome générique (lecture/écriture de fichiers, recherche, shell, git) avec boucle LLM, bac à sable et interface Streamlit.
2. **`prospection_wifi/`** — le tunnel métier de prospection Wi-Fi : scraping, nettoyage, enrichissement, scoring, rédaction et envoi d'e-mails.

---

## 2. Le tunnel `prospection_wifi`

Pipeline en dix étapes, chaque script lisant le CSV de l'étape précédente et écrivant le suivant :

| # | Script | Rôle | Service externe |
|---|---|---|---|
| 1 | `scraper.py` | Récupère les établissements (Google Maps) ou des profils LinkedIn | Apify |
| 1 bis | `clean_leads.py` | Exclut les catégories sans enjeu (pizzas à emporter, snacks…), 115 → 96 leads | — |
| 2 | `scorer.py` | Score d'achat par lead, tri par probabilité | TypeSafe (modèle Jev) |
| 3 | `emailer.py` | Rédige 3 e-mails personnalisés par lead (JSON strict) | DeepSeek |
| 4 | `enricher.py` | Cherche l'e-mail de contact sur le site web | — (requests + BeautifulSoup) |
| 5 | `enricher_hunter.py` | Complète les e-mails manquants par domaine | Hunter.io |
| 6 | `enricher_netanalyzer.py` | Croise avec les scans Wi-Fi (fabricant routeur, sécurité) | — (CSV NetAnalyzer) |
| 7 | `enricher_facebook.py` | Complète via les pages Facebook publiques | Apify (acteur Facebook) |
| 8 | `fusionner_emails.py` | Fusionne les e-mails des différentes passes, sans perte | — |
| 9 | `generer_campagne_terrain.py` | Liste de visite physique (établissements scannés sans e-mail) | — |
| 10 | `enrichir_adresses_terrain.py` | Ajoute l'adresse postale des visites | Apify (Google Maps) |

`dashboard.py` produit en plus un tableau de bord HTML autonome (`leads_scores.html`).

**Qualité du code :** configuration centralisée (`config.py`), écritures CSV atomiques, appels HTTP injectables pour les tests hors ligne, mode `--dry-run` sur chaque étape, docstrings détaillées, gestion des erreurs et des timeouts. C'est un code de niveau professionnel, nettement plus étoffé que mes scripts `ops/`.

**Coût :** six services payants ou freemium sont nécessaires (Apify, TypeSafe, Hunter.io, Brevo, DeepSeek, plus l'acteur LinkedIn). À budgéter avant toute réexécution.

---

## 3. Les interfaces

| Interface | Technologie | Usage réel |
|---|---|---|
| `app.py` | Streamlit | Chat pour l'**agent de code**, pas pour la prospection. Lance `src/agent.py` en sous-processus avec `--yes`. |
| `src/agent.py`, `src/ui.py` | CLI + REPL `rich` | Agent de code en terminal, sessions multi-tours, journal JSONL. |
| `prospection_wifi/dashboard.py` | HTML statique (pandas) | Tableau de bord des leads scorés, ouvrable sans serveur. |
| `generate_pdf.py` | Playwright | Export HTML → PDF du one-pager ATN. |
| `find_atn_emails.py` | CLI | Vérification d'adresses via l'endpoint `email-verifier` de Hunter. |

Il n'existe **pas** d'interface Streamlit pour la prospection : le tunnel se pilote en ligne de commande.

---

## 4. Comparaison avec les scripts `ops/`

| Besoin | `ops/` (existant) | `legacy-agent/` | Verdict |
|---|---|---|---|
| Génération de contenu LLM | `generate_article.py` — articles SEO, contrôle qualité, alerte Discord | `emailer.py` — 3 e-mails de prospection par lead | **Non redondant** : usages et prompts différents, même socle technique (SDK OpenAI + DeepSeek) |
| Alertes | `discord_alert.py` — webhook Discord, retries, validation | `sender.py` — envoi Brevo aux prospects | **Non redondant** : interne vs externe |
| Supervision | `check_server.py` — santé du portail + alerte | — | **Unique**, à conserver |
| Orchestration | `cron_weekly_article.sh` — cron, anti-doublon de sujets | — | **Unique**, à conserver |
| Agent de code | — (assuré par Hotumana / DSH) | `src/` + `app.py` + `src/ui.py` | **Redondant avec mon rôle** |
| Scraping / enrichissement / scoring | — | `scraper.py`, `enricher*.py`, `scorer.py` | **Unique et utile** |
| Nettoyage et consolidation de leads | — | `clean_leads.py`, `fusionner_emails.py` | **Utile** |
| Tableau de bord leads | — | `dashboard.py` | **Utile** (aucun équivalent `ops/`) |
| Export PDF | — | `generate_pdf.py` | **Utile** (aucun équivalent `ops/`) |
| Vérification d'e-mails | — | `find_atn_emails.py` | **Utile mais marginal** |

**Conclusion :** la redondance fonctionnelle est faible. Le seul vrai doublon est l'**agent de développement local**, qui refait ce que je fais déjà — en parallèle, avec ses propres garde-fous et son propre accès shell. La prospection, elle, couvre un besoin que `ops/` n'adresse pas du tout.

**Doublons de données :** 6 des 7 CSV déjà importés dans `03_Commercial_et_Prospection/1_Tableaux_Suivi/Donnees_Leads/` sont identiques (aux fins de ligne près) ; seul `campagne_terrain_adresses.csv` diffère. Les 10 autres CSV du dépôt sont des états intermédiaires du pipeline.

---

## 5. Ce qui est utile et à conserver

Par ordre de valeur :

1. **Le tunnel de prospection complet** (`prospection_wifi/`) — cœur de métier, réutilisable pour les futures campagnes.
2. **`dashboard.py`** — visualisation rapide des leads scorés, sans dépendance serveur.
3. **`clean_leads.py` et `fusionner_emails.py`** — fiabilisation de la base, indépendante des API payantes.
4. **`generate_pdf.py`** — génération de one-pagers PDF depuis le HTML, utile pour tous les supports commerciaux.
5. **`find_atn_emails.py`** — vérification ponctuelle d'adresses avant envoi.

## 6. Ce qui est redondant ou à archiver

1. **`src/` (agent autonome) + `app.py` + `src/ui.py`** — je remplis déjà ce rôle, avec le bac à sable de l'espace de travail et sans risque de double agent. À conserver comme référence/documentation, mais **à ne pas exécuter en parallèle**.
2. **`one_pager_atn.html` / `WaveFi_OnePager_ATN.pdf`** — le one-pager ATN est déjà dans `03_Commercial_et_Prospection/6_One_Pagers_et_Supports/`.
3. **Les CSV de leads** — à ne pas maintenir en double ; la source de vérité doit rester `Donnees_Leads/`.

---

## 7. Adaptations nécessaires avant un usage en production

| Sujet | Constat | Action recommandée |
|---|---|---|
| Configuration | `.env` propre au dépôt, `DEEPSEEK_MODEL=deepseek-chat` | Aligner sur `ops/deepseek.env` et le modèle `deepseek-flash`, ou documenter l'écart |
| Chemins | CSV lus/écrits dans le dossier courant | Accepter `--input/--output` partout, ou exécuter depuis `prospection_wifi/` |
| Python | Développé sous Python 3.9 / Windows | Vérifier sous Python 3.12+ ; adapter les docs PowerShell |
| Envoi | Brevo, `email_1` seulement, anti-doublon, créneaux mardi–jeudi | Conserver ; ajouter un registre d'opposition et une revue humaine avant envoi |
| Automatisation | Pipeline 100 % manuel | Ne **pas** planifier l'envoi ; éventuellement un cron de *préparation* + alerte Discord |
| Données | 17 CSV, 1,2 Mo, doublons | Source unique `Donnees_Leads/`, le reste en `Archives/` |
| Tests | Suite riche mais dépendances non installées sur le serveur | Créer un venv dédié et exécuter `pytest` avant adaptation |
| Licence | Aucune licence dans le dépôt | Décider du statut (privé) avant toute réutilisation externe |

---

## 8. Risques

### 8.1 Dépôt public avec données personnelles — **critique**

Le dépôt est public alors qu'il contient 96 leads nominatifs et des e-mails personnalisés.
Recommandations, dans l'ordre :

1. Passer le dépôt en **privé** immédiatement.
2. Si des données ne doivent jamais être publiques, purger l'historique (`git filter-repo`) — le simple passage en privé ne retire pas les copies déjà indexées ou clonées.
3. Sortir les CSV du versionnement (`.gitignore`) et les stocker uniquement dans `Donnees_Leads/`.

### 8.2 Interface Streamlit avec `--yes`

`app.py` lance l'agent avec `--yes`, ce qui **approuve d'avance toutes les commandes shell**. Combiné à l'injection des secrets Streamlit dans l'environnement du sous-processus, une interface exposée permettrait à un prompt malveillant d'exécuter des commandes et de lire les clés. À réserver à un usage local, sans déploiement public.

### 8.3 Conformité prospection

Les e-mails incluent un lien de désabonnement Brevo et un contrôle des créneaux, ce qui est un bon socle. Restent à formaliser : base légale du démarchage B2B, registre d'opposition, durée de conservation des leads, mention de l'origine des données.

### 8.4 Coûts API

Apify, TypeSafe, Hunter, Brevo et DeepSeek sont facturés à l'usage. Un `--limit` mal maîtrisé ou une réexécution complète peut coûter cher ; les modes `--dry-run` et `--limit` doivent être la norme.

---

## 9. Recommandation

**Conserver la prospection, archiver l'agent.**

1. Garder `prospection_wifi/` comme outil métier, documenté par un runbook `ops/runbook-prospection.md` (étapes, variables, coûts, précautions).
2. Ne pas exécuter `src/` ni `app.py` dans cet espace : mon rôle couvre déjà le développement et l'infrastructure, avec un sandbox unique.
3. Faire du dossier `Donnees_Leads/` la seule source de vérité pour les CSV.
4. Passer le dépôt en privé et sortir les données du versionnement.
5. Adapter ensuite, si tu valides : variables d'environnement unifiées, notification Discord en fin de pipeline (sans envoi automatique), et un `--input/--output` systématique.

---

## Annexe — repères

- Tester le nettoyage hors ligne : `cd ops/legacy-agent/prospection_wifi && python3 clean_leads.py --dry-run` → 115 lignes lues, 96 conservées, 19 exclues.
- Comparer les données : `Donnees_Leads/` (archive, 7 CSV) vs `prospection_wifi/` (17 CSV).
- Le dépôt ne contient ni `.env`, ni clé API, ni jeton dans son historique.
