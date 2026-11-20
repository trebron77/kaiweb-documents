# Rotation des clés — FenuaFact

> Créé le 2026-11-17. Les clés ont circulé en clair dans `main.py` avant la migration vers `.env`.
> Objectif : les remplacer **et révoquer les anciennes**.

## État d'avancement

| # | Service | État |
| --- | --- | --- |
| 1 | Supabase `service_role` | ✅ **fait** — ancienne clé refusée (vérifié) |
| 2 | Meta (token WhatsApp) | ✅ **fait** — nouveau token validé (numéro, `verified_name`, `/me`) |
| 3 | Groq | ✅ **fait** — 11 modèles accessibles via le SDK, dont `whisper-large-v3-turbo` |
| 4 | Brevo | ✅ **fait** — clé restreinte « Emails transactionnels », `400 sender is missing` |
| 5 | `VERIFY_TOKEN` | ✅ **fait** — ancien refusé (403), nouveau accepté (200). **Reste : re-vérifier le webhook dans Meta** |

### Notes issues de l'opération

- **Brevo** : la clé est restreinte aux emails transactionnels. `/v3/account` renvoie `403` — c'est normal. Brevo révoque toute clé inactive 90 jours : si le bot n'envoie rien pendant trois mois, il faudra recréer une clé.
- **Vérification d'une clé Brevo sans envoyer d'email** : `POST /v3/smtp/email` avec un corps vide → `400 sender is missing` si la clé est bonne, `401` sinon.
- **Vérification d'une clé Groq** : `GET /openai/v1/models` avec `curl` ou le SDK. Attention, `python-urllib` est bloqué par Cloudflare (403 code `1010`).

> ⚠️ Incident du 2026-11-17 : une commande d'exemple `sed` a été recopiée telle quelle, laissant `SUPABASE_KEY=TA_NOUVELLE_CLE` dans `.env`. L'API répondait `200` sur `/health` alors que toute lecture de base échouait. C'est pourquoi `check_health.py` vérifie désormais **aussi** l'accès Supabase (état `DB_KO`).

## Règle d'or

Une rotation n'est terminée que lorsque **l'ancienne clé est révoquée**. Créer une nouvelle clé sans supprimer l'ancienne ne protège de rien.

Après chaque étape :

```bash
systemctl restart fenuafact
curl -s https://api.fenuafact.com/health
```

## Ordre de priorité

| # | Service | Pourquoi d'abord |
| --- | --- | --- |
| 1 | **Supabase** `service_role` | Contourne toutes les RLS : accès total aux données clients |
| 2 | **Meta** (token WhatsApp) | Permet d'envoyer des messages en ton nom |
| 3 | **Groq** | Facturation à ton compte |
| 4 | **Brevo** | Envoi d'emails depuis ton domaine |
| 5 | `VERIFY_TOKEN` | Faible portée, mais public dans le chat |

---

## 1. Supabase — clé secrète

**Ne touche pas au « JWT secret ».** Le régénérer invaliderait la clé anonyme utilisée par le front et déconnecterait tous les utilisateurs. On remplace uniquement la clé secrète de service.

1. Dashboard Supabase → projet `ewlrfhkzojcjagobjdbd` → **Project Settings** → **API Keys**.
2. Créer une nouvelle clé **secret** (`sb_secret_…`).
3. La coller dans `.env` : `SUPABASE_KEY=...`
4. Redémarrer, vérifier `/health`.
5. **Révoquer l'ancienne** clé secrète dans le dashboard.

## 2. Meta — token WhatsApp

> **Meta ne permet pas de révoquer un token à l'unité.** Le bouton « Révoquer les tokens » invalide **tous** les tokens de l'utilisateur système, y compris celui qui vient d'être créé. La séquence est donc : **révoquer, puis générer, puis mettre à jour `.env`**. Le bot est hors service pendant ces deux minutes.

1. `business.facebook.com` → **Paramètres du compte professionnel** → **Utilisateurs** → **Utilisateurs système**.
2. Sélectionner l'utilisateur système, **Générer un nouveau token** avec la permission `whatsapp_business_messaging` (et `whatsapp_business_management`).
3. Mettre à jour `ACCESS_TOKEN` dans `.env`.
4. Redémarrer, puis envoyer un vocal de test : si le bot répond, le token est bon.
5. Dans l'app Meta → **WhatsApp → Configuration de l'API**, vérifier que l'ancien token n'est plus utilisé, puis le révoquer.

## 3. Groq

1. `console.groq.com/keys` → **Create API Key**.
2. Mettre à jour `GROQ_API_KEY` dans `.env`.
3. Redémarrer, puis envoyer un vocal de test (transcription + extraction).
4. **Supprimer l'ancienne clé** dans la console.

## 4. Brevo

1. `app.brevo.com` → **SMTP & API** → **API Keys** → créer une clé.
2. Mettre à jour `BREVO_API_KEY` dans `.env`.
3. Redémarrer, puis répondre à un devis avec une adresse email pour tester l'envoi.
4. **Supprimer l'ancienne clé**.

## 5. Verify token

Générer une valeur aléatoire :

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

1. Remplacer `VERIFY_TOKEN` dans `.env`.
2. Redémarrer.
3. Dans Meta → WhatsApp → Configuration → **Modifier** le webhook, saisir le nouveau token, **Vérifier et enregistrer**.

> Sans cette dernière étape, la vérification échouera si Meta redemande un jour à valider l'URL.

---

## Vérification finale

```bash
# 1. Service
systemctl is-active fenuafact
curl -s https://api.fenuafact.com/health

# 2. Webhook (remplace par le token du .env)
curl -s -o /dev/null -w '%{http_code}\n' \
  "https://api.fenuafact.com/webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=TON_TOKEN&hub.challenge=x"

# 3. Aucun secret en dur dans le code
grep -cE '(EAA|gsk_|sb_secret|xkeysib)' /var/www/fenuafact-api/main.py

# 4. Permissions du .env
stat -c '%a %n' /var/www/fenuafact-api/.env
```

Attendu : `active`, `{"status":"ok"}`, `200`, `0`, `600`.

## Test fonctionnel de bout en bout

Après les cinq rotations : envoyer un vocal WhatsApp et vérifier que le PDF arrive. C'est le seul test qui valide Meta + Groq + Supabase + Brevo d'un coup.
