# Projet WaveFi — dossier de travail

> Réorganisation effectuée le **14 novembre 2026**, puis fusion avec l'espace de travail multi-projets.
> Porteur du projet : **Norbert KAIMUKO** — contact@wavefi.tech — +689 87 70 01 79
> Entité en cours de constitution : **SASU KAIWEB MARKETING** (marque commerciale **WaveFi**).
> Solution de Wi-Fi marketing validée par la **DGEN** (Direction générale de l'économie numérique) en Polynésie française.

Liens utiles : [guide global de l'espace de travail](../../README.md) · [identité de l'agent](../../persona-hotumana.md).

---

## 1. Règles du dossier

1. **Aucun fichier n'a été supprimé.** Les pièces obsolètes sont conservées dans `Archives/`.
2. **Un fichier = un seul emplacement.** Les doublons constatés sont listés au §6, ils n'ont pas été supprimés sans accord.
3. **Nommage** : préfixes numériques (`01_`, `02_`…) pour figer l'ordre d'affichage ; périodes comptables en `AAAA-MM` ; un point de départ = un dossier de campagne ou de version.
4. **Fichiers système Windows** : `desktop.ini` est exclu de l'archive et n'a pas sa place sur le serveur.
5. **Pas de secret dans le dossier.** Les clés d'API vivent dans `ops/*.env` (exclus de la diffusion) ou dans un gestionnaire de secrets ; les runbooks ne citent que l'emplacement, jamais la valeur.

---

## 2. Arborescence

```text
projets-clients/wavefi/
├─ README.md                          ← ce fichier
├─ content/                           articles SEO (cible du générateur automatique)
├─ ops/                               scripts, runbooks, supervision, pipeline de prospection
├─ 01_Administratif_et_Juridique/
│  ├─ 1_Statuts_SASU/                 statuts, convention de compte courant, checklist CDFE
│  ├─ 2_Avocat/                       demande de devis, relance, projet relu
│  ├─ 3_Domiciliation/                Papeete Coworking (agrément, contrat, pièces d'identité)
│  ├─ 4_Banque/                       questions à l'ouverture du compte
│  ├─ 5_CDFE_JOPF/                    (vide — à remplir au dépôt du dossier)
│  ├─ 6_Assurances/                   (vide — RC Pro à souscrire)
│  └─ 7_Documents_Legaux_SaaS/
│     ├─ A_CGU_CGV_Clients_Finaux/    CGU/CGV + annexes clients finaux
│     ├─ B_Contrat_de_Revente_Revendeurs/  contrat de revente + annexes
│     └─ C_Versions_HTML_Site_Web/    versions HTML publiées sur le site
├─ 02_Produit_WaveFi/
│  ├─ FICHE_PRODUIT_WaveFi.md         synthèse produit, stack, plans
│  ├─ 1_Documentation_Technique/      (vide — specs, schémas, API)
│  ├─ 2_Design_et_UX/
│  │  ├─ Captures_Interface/          captures de l'application
│  │  └─ Maquettes_ATN/               maquettes accueil + connexion (Air Tahiti Nui)
│  └─ 3_Support_et_Bugs/              (vide — tickets, bugs, réclamations)
├─ 03_Commercial_et_Prospection/
│  ├─ Les 5 pilliers.html             stratégie : 5 piliers + partenariats
│  ├─ Stratégies- Les 5 pilliers & Partenariats.docx
│  ├─ WaveFi — Stratégie & Partenaires.pdf
│  ├─ 1_Tableaux_Suivi/
│  │  ├─ Tableau de suivi Prospection WaveFi.xlsx   ← fichier de suivi (mis à jour)
│  │  ├─ ETAT_PROSPECTION_2026-11-14.md             ← état des lieux écrit
│  │  ├─ Meilleurs période de prospection.xlsx
│  │  ├─ Donnees_Leads/               CSV de leads (voir §4)
│  │  └─ Archives_versions/           versions antérieures du tableau de suivi
│  ├─ 2_Pitchs_et_Scripts/            Pitch/, Script/, template de relance, séquences e-mail
│  ├─ 3_Prospects_Restos_Bars/        échanges nominatifs (HIP Lounge…)
│  ├─ 4_Prospects_Hotels/             (vide — aucun échange nominatif archivé)
│  ├─ 5_Partenaires_Techniques/       Infonecs, installateurs
│  ├─ 6_One_Pagers_et_Supports/       one-pagers PDF + HTML (générique, ATN, Port Autonome, lancement)
│  ├─ 7_Offre_et_Tarifs/              plans Free/Starter/Pro/Business, coût d'un set-up
│  └─ 8_Grands_Comptes/               fiches comptes et scripts d'appel (Port Autonome de Papeete)
├─ 04_Finance_et_Comptabilite/
│  ├─ 1_Abonnements_SaaS/2026-10/     OpenAI, paiement et hébergement SaaS
│  ├─ 2_Previsionnel/                 (vide — business plan chiffré)
│  ├─ 3_Facturation_Clients/          (vide — aucune facture client émise)
│  ├─ 4_Factures_Fournisseurs/
│  │  ├─ 2026-10/                     reçu photographié
│  │  └─ 2026-11/                     domiciliation Papeete Coworking (n° 11112026)
│  └─ 5_Devis_Fournisseurs/           devis reçus (S00107)
├─ 05_Marketing_et_Communication/
│  ├─ 1_Site_Vitrine/Verification_Google/   fichier de validation Search Console
│  ├─ 2_Reseaux_Sociaux/              (vide — visuels, calendrier éditorial)
│  ├─ 3_Veille_et_Concurrents/        MyWiFi Networks, playbook freelance, veille vidéo IA
│  └─ 4_Banniere_et_Logo/             bannières, logo, couverture KaiWeb Marketing
├─ 06_Suivi_Projet_et_Journal/
│  ├─ Journal_IA/                     transcriptions des sessions de build (SaaS, Cline)
│  └─ Reflexions/                     positionnement, identité professionnelle
└─ Archives/                          versions antérieures (documents légaux, statuts, one-pagers, legacy-agent)
```

`content/` et `ops/` sont les deux piliers de travail ajoutés à la structure du dossier : ils ne
suivent pas la numérotation pour rester compatibles avec les automatisations existantes
(le générateur d'articles écrit dans `content/`, les tâches cron appellent `ops/`).

---

## 3. Où trouver quoi

| Besoin | Emplacement |
|---|---|
| Faire le point sur les prospects | `03_Commercial_et_Prospection/1_Tableaux_Suivi/` |
| Envoyer un one-pager à un prospect | `03_Commercial_et_Prospection/6_One_Pagers_et_Supports/` |
| Préparer un appel grand compte (PAP…) | `03_Commercial_et_Prospection/8_Grands_Comptes/` |
| Connaître les tarifs | `03_Commercial_et_Prospection/7_Offre_et_Tarifs/` |
| Reprendre un message de relance | `03_Commercial_et_Prospection/2_Pitchs_et_Scripts/` |
| Relancer l'avocat / la domiciliation | `01_Administratif_et_Juridique/2_Avocat/`, `.../3_Domiciliation/` |
| Publier les pages légales du site | `01_Administratif_et_Juridique/7_Documents_Legaux_SaaS/C_Versions_HTML_Site_Web/` |
| Retrouver une facture d'abonnement | `04_Finance_et_Comptabilite/1_Abonnements_SaaS/` |
| Retrouver les captures de l'app | `02_Produit_WaveFi/2_Design_et_UX/Captures_Interface/` |
| Comprendre l'historique du build | `06_Suivi_Projet_et_Journal/Journal_IA/` |
| Lire ou publier un article SEO | `content/` |
| Diagnostiquer une alerte ou une sauvegarde | `ops/` et ses runbooks |
| Lancer une campagne de prospection | `ops/runbook-prospection.md` (pipeline dans `ops/legacy-agent/prospection_wifi/`) |
| Envoyer le bilan d'une campagne sur Discord | `python3 ops/notify-prospection.py` |

---

## 4. Données de leads (copiées le 14/11/2026)

Ces CSV proviennent du projet Python `local-dev-agent-01\prospection_wifi`
(copiés **sans modifier l'original**, qui reste sur le Bureau) :

| Fichier | Contenu |
|---|---|
| `leads_polynesie_filtres.csv` | 96 leads qualifiés Polynésie (15 colonnes) |
| `leads_scores.csv` | 96 leads avec score d'achat, probabilité, cas d'usage, priorité |
| `leads_enrichis_globaux.csv` | 96 leads enrichis e-mail (22 colonnes) |
| `campagne_terrain.csv` | 19 établissements de la campagne terrain (routeur, sécurité WiFi) |
| `campagne_terrain_adresses.csv` | les 19 mêmes établissements + adresse postale |
| `campagne_wifi_master_propre.csv` | 90 fiches master nettoyées (avec e-mails type) |
| `brevo_import.csv` | 7 contacts prêts à importer dans Brevo |

Le point commercial complet (chiffres, état prospect par prospect, actions) est dans
[`ETAT_PROSPECTION_2026-11-14.md`](03_Commercial_et_Prospection/1_Tableaux_Suivi/ETAT_PROSPECTION_2026-11-14.md).

---

## 5. Contenu SEO et automatisations

### Articles disponibles (11)

| Article | Cible |
|---|---|
| [`article-restaurant.md`](content/article-restaurant.md) | restaurants (avis Google à Tahiti) |
| [`article-centre-commercial.md`](content/article-centre-commercial.md) | centres commerciaux |
| [`article-fast-food.md`](content/article-fast-food.md) | fast-foods et franchises |
| [`article-hotellerie.md`](content/article-hotellerie.md) | hôtellerie (Polynésie) |
| [`article-le-wi-fi-marketing-pour-les-aeroports-et-terminaux-de-croisiere-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-aeroports-et-terminaux-de-croisiere-en-polynesie.md) | aéroports et terminaux de croisière |
| [`article-le-wi-fi-marketing-pour-les-agences-immobilieres-a-tahiti.md`](content/article-le-wi-fi-marketing-pour-les-agences-immobilieres-a-tahiti.md) | agences immobilières |
| [`article-le-wi-fi-marketing-pour-les-banques-et-agences-d-assurance-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-banques-et-agences-d-assurance-en-polynesie.md) | banques et assurances |
| [`article-le-wi-fi-marketing-pour-les-compagnies-aeriennes-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-compagnies-aeriennes-en-polynesie.md) | compagnies aériennes |
| [`article-le-wi-fi-marketing-pour-les-hopitaux-et-cliniques-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-hopitaux-et-cliniques-en-polynesie.md) | hôpitaux et cliniques |
| [`article-le-wi-fi-marketing-pour-les-institutions-publiques-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-institutions-publiques-en-polynesie.md) | institutions publiques |
| [`article-le-wi-fi-marketing-pour-les-salles-de-sport-et-studios-de-crossfit-en-polynesie.md`](content/article-le-wi-fi-marketing-pour-les-salles-de-sport-et-studios-de-crossfit-en-polynesie.md) | salles de sport et studios CrossFit |

Règles éditoriales : mentions locales exactes, validation DGEN sans sur-répétition, aucun chiffre non sourcé, CTA vers `contact@wavefi.tech`.

### Automatisations en place

| Script | Déclenchement | Rôle |
|---|---|---|
| `ops/check_server.py` | cron, tous les jours à 18:00 UTC (08:00 Tahiti) | Vérifie la disponibilité du portail et alerte sur Discord en cas d'échec. |
| `ops/cron_weekly_article.sh` | cron, lundi à 18:00 UTC (08:00 Tahiti) | Choisit un sujet inédit et lance la génération d'un article SEO dans `content/`. |
| `ops/generate_article.py` | appelé par le script ci-dessus | Rédige l'article via l'API DeepSeek, l'écrit dans `content/`, puis alerte Discord. |
| `ops/discord_alert.py` | appelé par les scripts ci-dessus | Envoie un message sur le webhook Discord configuré. |

Runbooks : [`ops/runbook-supervision-openwisp.md`](ops/runbook-supervision-openwisp.md) et
[`ops/runbook-alertes-discord.md`](ops/runbook-alertes-discord.md).

### Prospection (manuel, sans envoi automatique)

Le tunnel historique vit dans `ops/legacy-agent/prospection_wifi/` : scraping, nettoyage, scoring,
rédaction et enrichissement des e-mails. Il se pilote **à la main**, étape par étape, avec
`--dry-run` puis `--limit`.

- Procédure complète : [`ops/runbook-prospection.md`](ops/runbook-prospection.md).
- Bilan de fin de pipeline : `python3 ops/notify-prospection.py` (compteurs uniquement, via Discord).
- `sender.py` n'est **jamais** planifié : l'envoi Brevo reste une décision manuelle, journalisée
  avec `--sent-log`.
- Les CSV de leads sont ignorés par Git et restent en local ; ne pas les publier.
- L'agent de code (`src/`, `app.py`) est archivé dans `Archives/legacy-agent/` et n'est pas exécuté.

> Les tâches cron historiques appellent `workspace/ops/...` ; un lien symbolique `workspace/ops`
> pointe vers ce dossier. La migration est décrite dans le [README global](../../README.md).

---

## 6. Points à valider / doublons signalés (non supprimés)

**Statuts de prospection à confirmer** (voir `ETAT_PROSPECTION_2026-11-14.md`) :
- HIP Lounge : message + relance rédigés le 27/10 → envoi à confirmer.
- Infonecs / Next Informatique : contactés les 17 et 19/10, relance 72 h **dépassée**.
- ADT, Air Tahiti Nui : dossiers prêts, statut « à contacter » tant que l'envoi n'est pas confirmé.
- Port Autonome de Papeete : **contact établi le 12/11** (appel + mail au commandant, one-pager et maquette du portail TCI envoyés) ; rendez-vous de 15 min à caler — voir [`8_Grands_Comptes/`](03_Commercial_et_Prospection/8_Grands_Comptes/).

**Doublons ou quasi-doublons constatés** :
1. `Annexe 2 Politique Cookies v1.1.html` existe en `C_Versions_HTML_Site_Web/` **et** en `A_CGU_CGV_Clients_Finaux/` (contenu identique, 16 Ko).
2. `7-Politique de remboursement v1.1.docx` est présent dans `A_…` **et** dans `B_…`.
3. `Infonecs 1ère approche.md` et `Infonecs 1ère approche.txt` : même contenu, deux formats.
4. `contrat-revente.html` (09/10) et `Contrat de revente SaaS v1.1.html` (11/10) : deux générations.
5. `politique-remboursement.html` (09/10) et `Politique de remboursement v1.1.html` (11/10).
6. Deux exemplaires du projet de contrat de domiciliation (13/11 et 12/11, tailles différentes).
7. `Archives/CGU-CGV & annexes/Fichier - Exporter en PDF/` contient des copies des `.docx` courants.
8. `Satut SASU.docx` dans `Archives/` est une faute de frappe pour `Statut SASU.docx` (version d'archive).
9. One-pager Port Autonome de Papeete : la version PDF de référence (2 pages, 12/11 18:29) est dans `6_One_Pagers_et_Supports/` ; la génération antérieure (HTML + PDF 1 page, 12/11 15:42) est archivée dans `Archives/One_Pagers_v1_2026-11-12/`.

**Dossiers encore vides** (structure prête, à alimenter) : `1_Documentation_Technique`,
`3_Support_et_Bugs`, `4_Prospects_Hotels`, `2_Reseaux_Sociaux`, `2_Previsionnel`,
`3_Facturation_Clients`, `5_CDFE_JOPF`, `6_Assurances`.

---

## 7. Journal des réorganisations

### 14/11/2026 — réorganisation du dossier d'origine

| Avant | Après |
|---|---|
| `HTML/` (20 pages) | réparties : légal → `01_…/7_Documents_Legaux_SaaS/C_Versions_HTML_Site_Web/`, statuts → `01_…/1_Statuts_SASU/`, one-pagers → `03_…/6_One_Pagers_et_Supports/`, stratégie → `03_…/` |
| `Chat réplique/` (5 transcriptions) | `06_Suivi_Projet_et_Journal/Journal_IA/` |
| `SEO_GEO/google…html` | `05_…/1_Site_Vitrine/Verification_Google/` |
| `SaaS Founder.txt` | `06_…/Reflexions/` |
| `Résume moi cette vidéo.txt` | `05_…/3_Veille_et_Concurrents/` |
| `Mywifi features.docx` | `05_…/3_Veille_et_Concurrents/` |
| `4._Bannière & logo/` | renommé `4_Banniere_et_Logo/` ; les 6 captures produit sont parties en `02_…/2_Design_et_UX/Captures_Interface/` |
| `wavefi_maquette_*.jpg` (2) | `02_…/2_Design_et_UX/Maquettes_ATN/` |
| One-pagers PDF épars (5) | `03_…/6_One_Pagers_et_Supports/` |
| `. WaveFi plan script Dodo t.txt` | `03_…/7_Offre_et_Tarifs/WaveFi - Plans et tarifs (Dodo).txt` |
| `Oen_pager lancement_30_jrs_gratuit.pdf` | `03_…/6_One_Pagers_et_Supports/One-Pager - Lancement 30 jours gratuits.pdf` |
| `Calcul du coût d'un set-up WaveFi.txt` | `03_…/7_Offre_et_Tarifs/` |
| `Template relance email & whatsapp-sms message.docx` | `03_…/2_Pitchs_et_Scripts/` |
| `Meilleurs période de prospection.xlsx` | `03_…/1_Tableaux_Suivi/` |
| `Fidéliance. Demande de devis — Domiciliation.txt` | `01_…/3_Domiciliation/` (mal classé en « partenaires techniques ») |
| `PROJET CONTRAT DE DOMICILIATION ENTREPRISE(1).pdf` | `01_…/3_Domiciliation/Papeete Coworking/Projet contrat domiciliation (exemplaire 12-11).pdf` |
| `Factures SASU/` (abonnements + domiciliation mêlés) | factures SaaS → `1_Abonnements_SaaS/2026-10/`, domiciliation → `4_Factures_Fournisseurs/2026-11/` |
| `Devis SASU/` | `5_Devis_Fournisseurs/` |
| `2_…/4_Support_et_Bugs/` | renommé `3_Support_et_Bugs/` (numérotation continue) |

### 14/11/2026 — intégration à l'espace de travail

- Import de l'archive `projet_wavefi_propre.zip` (156 fichiers) dans `projets-clients/wavefi/`, en conservant la structure en six catégories.
- Fusion de l'ancien dossier `b2b-outbound/` : les deux séquences e-mail rejoignent `03_…/2_Pitchs_et_Scripts/`, l'état de la prospection est fusionné dans `ETAT_PROSPECTION_2026-11-14.md` (§6), l'ancien one-pager Port Autonome est archivé.
- Suppression des dossiers vides hérités de l'organisation précédente (`growth/`, `product/`, `legal/`, `hardware/`, `b2b-outbound/`) : leur contenu est couvert par les catégories numérotées.
- L'archive d'origine est conservée dans `Archives/projet_wavefi_propre_2026-11-14.zip`.

### 14/11/2026 — intégration de l'agent local historique

- Dépôt `wavefi-prospection` (anciennement `local-dev-agent-01`) cloné dans `ops/legacy-agent/`.
- Pipeline de prospection conservé et documenté par `ops/runbook-prospection.md`.
- Agent de code (`src/`, `app.py`, tests associés) déplacé dans `Archives/legacy-agent/`, sans exécution.
- CSV de leads retirés du suivi Git et ajoutés au `.gitignore` (fichiers conservés localement).
- Ajout de `ops/notify-prospection.py` : bilan de fin de pipeline sur Discord, sans envoi d'e-mails.
- L'historique Git distant n'a pas été purgé : les commandes sont préparées dans le runbook (§5).

---

## 8. Priorité actuelle

1. **Prospection** : relancer Infonecs, Next Informatique et HIP Lounge ; une demi-journée terrain à Papeete centre ; envoyer les one-pagers ATN et Port Autonome.
2. **Contenu** : publier les 11 articles SEO déjà rédigés.
3. **Produit** : alimenter `1_Documentation_Technique/` et `3_Support_et_Bugs/`.
4. **Petits commerces** : ne rien envoyer avant réception et test du kit routeur GL.iNet (voir §6 de l'état de prospection).
