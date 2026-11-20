# FenuaFact — état technique et runbook

> Vérifié le 2026-11-17 à 01:51 UTC, après remise en service de l'API.

## 1. Où tourne quoi

| Composant | Emplacement | Détail |
| --- | --- | --- |
| API FastAPI | `/var/www/fenuafact-api/main.py` | 336 lignes, Python 3.14.4 (venv local) |
| Service systemd | `/etc/systemd/system/fenuafact.service` | `Restart=always`, `enabled` |
| Processus | uvicorn | `127.0.0.1:8001` (jamais exposé directement) |
| Reverse proxy | Nginx | `api.fenuafact.com` → `proxy_pass http://127.0.0.1:8001` |
| TLS | Certbot | renouvellement automatique |
| Données | Supabase managé | `tenants`, `catalogue`, `devis` |
| Transcription | Groq `whisper-large-v3-turbo` | langue `fr` |
| Extraction | Groq `openai/gpt-oss-120b` | sortie JSON stricte |
| PDF | `fpdf2` | généré en local dans le dossier de l'app |
| Email | Brevo API v3 | pièce jointe base64 |
| WhatsApp | Meta Cloud API | `phone_number_id` dédié |

## 2. Commandes d'exploitation

```bash
# État du service
systemctl status fenuafact --no-pager

# Redémarrer après modification
python3 -c "import ast; ast.parse(open('/var/www/fenuafact-api/main.py').read())"  # syntaxe d'abord
systemctl restart fenuafact

# Logs en direct
journalctl -u fenuafact -f

# Vérifier que le webhook répond (403 attendu avec un faux token)
curl -s -o /dev/null -w '%{http_code}\n' \
  'https://api.fenuafact.com/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=test&hub.challenge=x'
```

## 2 bis. Documents : devis et factures

La table `devis` porte **les deux types** de document (`type_document` = `devis` | `facture`).

| Colonne ajoutée (2026-11-17) | Rôle |
| --- | --- |
| `numero` | `DEV-2026-0001` / `FAC-2026-0001`, unique par entreprise |
| `type_document` | `devis` ou `facture` |
| `parent_id` | devis d'origine d'une facture |
| `date_emission` / `date_echeance` | dates imprimées sur le PDF |
| `pdf_path` | chemin du PDF dans `media/` |

**Numérotation** : fonction SQL `next_document_number(tenant, type, année)`, atomique via `insert … on conflict do update … returning`. Le compteur est stocké dans `document_counters` (RLS activée, accès réservé au `service_role`). Un numéro n'est attribué qu'au moment où le document est réellement créé — pas de trou.

**Endpoints** :

| Méthode | Route | Rôle |
| --- | --- | --- |
| `POST` | `/api/devis/{id}/facture` | convertit un devis en facture numérotée + PDF |
| `GET` | `/api/documents/{id}/pdf` | renvoie le PDF (devis ou facture) |
| `POST` | `/api/relance` | relance email Brevo |

**Migration appliquée** : `ops/migrations/2026-11-17_facture_numerotation.sql` (jouée dans Supabase le 2026-11-17).

**Première facture réelle** : `FAC-2026-0001`, devis « Mme Marie » (4 h × 5 500 + déplacement 1 500 = 23 500 HT, TVA 13 % = 3 055, TTC 26 555 F), échéance 17/12/2026.

**Données corrigées le 2026-11-17** : entreprise renommée **KaiWeb Marketing**, téléphone WhatsApp `+689 87045105` (identifiant l'artisan), email `nkaimuko@gmail.com`. `numero_tahiti` reste `123456` — valeur de test à remplacer par le vrai numéro TAHITI avant production.

## 2 ter. Abonnement et paiement (Dodo Payments)

**Environnement actif : LIVE** (`https://live.dodopayments.com`). Le mode test reste configuré dans `.env.test`.

| Élément | Valeur |
| --- | --- |
| Produit Essentiel | `pdt_0NsEqzCgYeffcqEO2uWgz` — 7 950 XPF/mois |
| Produit Pro | `pdt_0NsEraHrapqMl6mlvENVD` — 12 900 XPF/mois |
| Marque Dodo | FenuaFact (secondaire, sous le même business que WaveFi) |
| Webhook | `https://api.fenuafact.com/webhooks/dodo` (mode réel) |

### Endpoints

| Méthode | Route | Rôle | Auth |
| --- | --- | --- | --- |
| `POST` | `/api/abonnement/checkout` | crée une session de paiement | JWT Supabase obligatoire |
| `POST` | `/api/abonnement/changer-plan` | montée/descente en gamme | JWT Supabase |
| `POST` | `/webhooks/dodo` | événements d'abonnement | signature Standard Webhooks |

Le JWT est validé auprès de Supabase, puis l'entreprise est résolue via `profiles.tenant_id`.

### Règles implémentées

- **Montée en gamme** : application immédiate, prorata facturé (`prorated_immediately`).
- **Descente en gamme** : programmée à la prochaine échéance (`next_billing_date`), aucun prélèvement immédiat — le client garde l'offre supérieure jusqu'à la fin de la période payée.
- **Un échec de paiement n'annule jamais un abonnement en cours** : les événements négatifs ne s'appliquent que s'ils concernent le `subscription_id` enregistré.
- **Le statut réel est lu dans le payload** (`data.status`), pas déduit du nom de l'événement — sans quoi `subscription.updated` réactivait un abonnement annulé.
- **Le plan vient des métadonnées** de la session de checkout (`metadata.plan`).
- **Relances automatiques** : réservées à `abonnement_plan = 'pro'` **et** `abonnement_statut = 'actif'`.

### Colonnes ajoutées à `tenants`

`abonnement_statut` (aucun · actif · en_retard · suspendu · annule · expire) · `abonnement_fin` · `abonnement_plan` (essentiel · pro) · `dodo_customer_id` · `dodo_subscription_id`.

Migrations : `2026-11-17_abonnement.sql`, `2026-11-18_plan.sql`.

### Points de vigilance

- La clé API live exige une **IP allowlist** contenant à la fois l'IPv4 (`194.163.44.206`) et l'IPv6 (`2a02:4780:10:503c::1`) du VPS — le serveur sort en IPv6 par défaut.
- La clé doit avoir **Abonnements → Écriture** pour le changement d'offre (et non seulement Lecture).
- Retour au mode test : `cp .env.test .env && systemctl restart fenuafact`.
- Un abonnement live non annulé est prélevé chaque mois : ne jamais en créer un pour une démonstration.
- **Changement d'offre non validé sur abonnement actif** (2026-11-18) : l'endpoint, le JWT et les paramètres Dodo sont corrects, mais le test de bout en bout reste à faire en mode test avec une carte fictive. Codes d'erreur déjà rencontrés et corrigés : `INVALID_PRORATION_MODE_WITH_NEXT_BILLING_DATE` (descente : `full_immediately` obligatoire) et `INACTIVE_SUBSCRIPTION_PLAN_CHANGE_NOT_SUPPORTED` (abonnement annulé).

## 3. Règle de déploiement

**Toujours vérifier la syntaxe avant de redémarrer.** La panne du 2026-11-17 venait d'une virgule manquante (ligne 276) : `Restart=always` a masqué l'échec en boucle de redémarrage, et l'API est restée muette plus d'une heure sans alerte.

```bash
cd /var/www/fenuafact-api
cp -a main.py "main.py.bak.$(date +%Y%m%d-%H%M%S)"
python3 -c "import ast; ast.parse(open('main.py', encoding='utf-8').read())" && systemctl restart fenuafact
```

## 4. Secrets — ✅ migrés le 2026-11-17

Les secrets ne sont **plus dans `main.py`**. Ils vivent dans `/var/www/fenuafact-api/.env` (`chmod 600`), chargé par un lecteur intégré (aucune dépendance ajoutée) :

```python
_load_env(Path(__file__).with_name(".env"))
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]   # échec au démarrage si absent
```

| Fichier | Rôle |
| --- | --- |
| `.env` | valeurs réelles — **600**, jamais versionné |
| `.env.example` | modèle à recopier, sans valeur |
| `.gitignore` | exclut `.env`, `venv/`, `__pycache__/`, `*.ogg`, `*.pdf`, `main.py.bak.*` |

Variables gérées : `VERIFY_TOKEN`, `PHONE_NUMBER_ID`, `ACCESS_TOKEN`, `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `BREVO_API_KEY`, `TENANT_ID`.

Vérifié après migration : webhook local **200**, webhook public **200**, service `active`.

### Reste à faire : rotation des clés

Les valeurs ont circulé dans un fichier non protégé (et le verify token apparaît dans les logs uvicorn). À renouveler, puis mettre à jour `.env` et redémarrer :

1. **Meta** — régénérer le token système du compte WhatsApp Business (et changer `VERIFY_TOKEN`).
2. **Groq** — révoquer `gsk_…`, créer une nouvelle clé.
3. **Supabase** — régénérer la clé `service_role` (elle **contourne toutes les RLS**).
4. **Brevo** — révoquer `xkeysib-…`, créer une nouvelle clé API.

> Après rotation : `systemctl restart fenuafact` puis rejouer le test du webhook.

### À faire ensuite : ne plus logger le token

Le `VERIFY_TOKEN` apparaît en clair dans `journalctl` parce que Meta le passe en paramètre d'URL. Prévoir `--no-access-log` sur uvicorn, ou un token court et rotationnable.

## 5. Dettes — état au 2026-11-17

| # | Dette | État |
| --- | --- | --- |
| 1 | Secrets en clair | ✅ Migrés en `.env`. **Reste : rotation des clés** (§4) |
| 2 | `TENANT_ID` en dur | ✅ Résolu : résolution par le numéro WhatsApp de l'artisan (`tenants.telephone`). **Reste : renseigner ce champ** pour chaque entreprise |
| 3 | `LAST_PDF` en mémoire | ✅ Persisté dans `media/last_pdf.json`, rechargé au démarrage |
| 4 | Fichiers `.ogg`/`.pdf` épars | ✅ Déplacés dans `media/` (24 fichiers) + **purge cron au-delà de 30 jours** |
| 5 | Signature webhook | ✅ Code en place (`X-Hub-Signature-256`, HMAC-SHA256). **Reste : renseigner `META_APP_SECRET`** dans `.env` |
| 6 | Erreurs techniques renvoyées au client | ✅ Message générique + `logger.exception` (trace côté serveur) |
| 7 | CORS `*` | ✅ Restreint à `ALLOWED_ORIGINS` (front Lovable + localhost en dev) |
| 8 | Aucun healthcheck | ✅ `GET /health` + **surveillance toutes les 5 minutes avec alerte Discord** |

### Détail des corrections appliquées

- **Médias** : tous les `.ogg` et `.pdf` sont écrits dans `media/`, plus dans le répertoire de l'application.
- **Signature** : si `META_APP_SECRET` est renseigné, toute requête dont la signature ne correspond pas est rejetée en **403**. Tant que la variable est vide, la vérification est ignorée (comportement d'attente, à ne pas laisser en production).
- **Erreurs** : le client WhatsApp reçoit « Une erreur technique est survenue », la trace complète va dans `journalctl`.
- **CORS** : seule l'origine du front est autorisée — vérifié : origine Lovable acceptée, origine inconnue refusée.

### Tests de non-régression (2026-11-17, après modifications)

```text
GET  /health                                   → 200 {"status":"ok"}
GET  /webhooks/whatsapp (bon token)            → 200
GET  /webhooks/whatsapp (mauvais token)        → 403
POST /webhooks/whatsapp (payload neutre)       → 200
CORS origine Lovable                           → header autorisé
CORS origine inconnue                          → refusé
```

### Supervision et purge (en place depuis le 2026-11-17)

| Tâche | Horaire | Effet |
| --- | --- | --- |
| `check_health.py` | toutes les 5 min | interroge `/health` ; alerte Discord **sur changement d'état** seulement (panne ou retour à la normale) |
| Purge médias | 03:15 chaque jour | supprime `.ogg` et `.pdf` de plus de 30 jours dans `media/` |
| Purge sauvegardes | 04:00 chaque jour | supprime les `main.py.bak.*` de plus de 60 jours |

- Journal : `ops/health.log`, état mémorisé : `ops/.health_state`.
- Webhook : `ops/discord.env` (600), même canal que WaveFi.
- Test manuel : `python3 check_health.py` ; simulation de panne : `HEALTH_URL=http://127.0.0.1:9/health python3 check_health.py --dry-run`.

**Limite connue** : si la syntaxe casse au redémarrage, l'alerte part bien, mais elle ne répare rien — elle prévient, c'est déjà l'essentiel.

### Multi-tenant : comment le bot reconnaît l'artisan

Décision du 2026-11-17 : **identification par le numéro WhatsApp de l'artisan**.

1. Meta transmet le numéro de l'expéditeur (`from`), souvent en chiffres sans `+`.
2. `normalize_phone()` ne garde que les chiffres : `+689 87 12 34 56` → `68987123456`.
3. `resolve_tenant()` compare ce numéro à `tenants.telephone` (tolérance sur le préfixe pays).
4. Numéro inconnu → réponse : « Ce numéro n'est pas encore associé à un compte FenuaFact ».
5. **Repli pilote** : s'il n'existe qu'un seul tenant en base et qu'aucun numéro ne correspond, on l'utilise en le signalant dans les logs. Dès qu'un deuxième tenant est créé, le repli disparaît : chaque entreprise **doit** avoir son `telephone` renseigné.

À faire côté données : renseigner `tenants.telephone` pour chaque entreprise. Le dashboard Lovable devra exposer ce champ dans les paramètres.

### Reste à faire

1. **Rotation des 5 clés** (§4) — priorité.
2. **`META_APP_SECRET`** : Meta → Paramètres de l'app → Clé secrète, à coller dans `.env` puis redémarrer.
3. **Renseigner `tenants.telephone`** pour chaque entreprise (sinon le repli pilote reste actif).
4. **Exposer le champ téléphone** dans les paramètres du front Lovable.
5. **Facture et numérotation** : conversion devis→facture, `DEV-2026-0001` sans trou.

## 6. Incident du 2026-11-17

- **Symptôme** : service `failed`, 5 redémarrages en boucle, bot muet depuis 00:44 UTC.
- **Cause** : `SyntaxError` ligne 276 — `"notes": devis_data.get("notes")` sans virgule avant `"statut": "Envoyé"`.
- **Correctif** : virgule ajoutée, syntaxe validée, service redémarré à 01:51 UTC.
- **Sauvegarde** : `main.py.bak.20261117-015113`.
- **Vérification** : webhook 200 avec le bon token, 403 avec un faux ; port 8001 en écoute.
- **Leçon** : aucun healthcheck, aucune alerte — d'où la priorité 8 ci-dessus.
