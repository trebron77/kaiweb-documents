# État de la configuration Meta / WhatsApp — WaveFi

> À remplir le 22/11/2026. Objectif : reconstituer ce qui a déjà été fait avec DeepSeek, afin de
> ne pas recréer ce qui existe. Numéro concerné : **+689 89 63 73 06**.

## 1. Le numéro est DÉJÀ sur l'API — établi le 22/11/2026

**Preuve :** le 23/10/2026 à 17h16, un message « Bonjour, ceci est un message de test envoyé depuis
votre application WaveFi » a été reçu sur le téléphone personnel de Norbert. Il a été émis par
l'application via l'API Meta — ce qui suppose un `phone_number_id` et un jeton valides. La
conversation porte en outre la mention *« Cette entreprise utilise un service sécurisé de la société
Meta pour gérer cette discussion »*, propre aux comptes gérés par l'API.

→ **Aucune migration à faire. Ne pas refaire l'onboarding : cela créerait un doublon.**
→ Le téléphone inutilisé n'a pas besoin d'être allumé ; il ne contient aucune application Meta.

## 2. Meta Business Manager — *à compléter depuis le tableau de bord*

| Question | Réponse |
|---|---|
| Une **application Meta** existe-t-elle pour WaveFi ? (nom + ID) | ✅ **Wavefi — App ID `1799972834584063`**, statut *Publiée*, cas d'usage WhatsApp actif |
| Un **compte WhatsApp Business (WABA)** existe-t-il ? | ................ |
| Le numéro +689 89 63 73 06 y est-il enregistré, avec un `phone_number_id` ? | en cours de relevé |
| Nom d'affichage / `verified_name` | ................ |
| Un **jeton d'accès** (system user token) existe-t-il ? *(ne pas écrire sa valeur)* | ................ |
| Un **webhook** est-il configuré ? | ................ |
| Statut de la **vérification d'entreprise** | ................ |

## 3. Ce qui est certain à ce jour

- Vérification d'entreprise : **en cours**.
- Le numéro est le seul dédié à WaveFi.
- FenuaFact utilise un numéro distinct (`87…`) — aucune interférence.

## 4. À décider après reconstitution

- Migrer le numéro vers l'API (seulement s'il est encore dans l'app).
- Créer ou récupérer l'application Meta, puis donner à Lovable les identifiants (jamais les secrets).

## Identifiants Meta — valeurs confirmées

| Objet | Identifiant | Remarque |
|---|---|---|
| Application Meta | `1799972834584063` | « Wavefi », publiée |
| **Compte WhatsApp Business — WaveFi** | **`1002263869569248`** | ✅ **le vrai WABA du numéro** — c'est celui que l'API attend |
| Test Messaging Account | `4626997277626482` | compte de test Meta, créé par défaut. **Ne pas l'utiliser** |
| Business Manager | `1817199402744833` | `business_id`. **Ne pas l'utiliser comme WABA** — il ne connaît pas `message_templates` |
| Numéro WaveFi | `+689 89 63 73 06` | qualité « Élevée » au 24/11 |
| **`phone_number_id`** | **`1437401462784496`** | relevé sur WhatsApp Manager → Numéros de téléphone |

### Piège rencontré le 24/11/2026

`META_WABA_ID` contenait une valeur erronée (Business Manager ou `phone_number_id`). L'appel
`GET /{wabaId}/message_templates` renvoyait alors :

```
HTTP 400 — OAuthException — code 100
(#100) Tried accessing nonexisting field (message_templates)
```

**Signature à retenir :** le code `100` sur `message_templates` signifie presque toujours **mauvais
type d'objet**, pas un problème de permission. Un `403` / code `200` signifierait, lui, une permission
`whatsapp_business_management` absente du jeton.

---

## Le lien d'abonnement manquant — 27/11/2026

### Le symptôme

L'envoi fonctionnait parfaitement : modèles approuvés, campagne envoyée, message reçu sur le
téléphone, quota consommé. Mais **rien n'entrait** : pas de confirmations de livraison, pas de
réponses de clients, pas de STOP traité.

### Pourquoi aucune des pistes habituelles ne marchait

| Suspect | Constat |
|---|---|
| L'URL de rappel | correcte : `https://app.wavefi.tech/api/public/whatsapp/webhook` |
| Le champ `messages` | abonné dans la console Meta |
| `META_WABA_ID` | contenait encore le compte de test — corrigé, sans effet |
| Le code du webhook | recevait et journalisait correctement (un échantillon envoyé depuis la console a produit un 403 journalisé, avec l'identifiant reçu) |
| L'application | publiée, joignable, répondait 200 |

Autrement dit : tout était bon, et rien n'arrivait.

### La vraie cause

L'application n'était **abonnée à aucun** compte WhatsApp Business. Ce lien (`subscribed_apps`) est
distinct de l'abonnement aux champs du webhook : sans lui, Meta ne délivre aucun événement, même si
l'URL répond.

Indice décisif : la seule ligne présente en base datait du 22 octobre et portait un identifiant de
test manuel. **Aucun événement réel n'avait jamais été reçu.**

### Le correctif — deux commandes

L'interface Business Manager était bloquée par une vérification d'identité impossible à valider (le
formulaire était verrouillé sur un ancien numéro inactif de Nouvelle-Calédonie, champ non
modifiable). La voie API restait : elle exige `whatsapp_business_management`, que le jeton de
production n'a pas — mais le **jeton temporaire généré depuis « Étape 1. Faites un essai »** le porte.

Depuis la console du VPS, avec ce jeton :

```bash
curl -s "https://graph.facebook.com/v21.0/1002263869569248?fields=id,name" \
  -H "Authorization: Bearer $TOKEN"
# → {"id":"1002263869569248","name":"WaveFi"}   (le compte existe et le jeton le voit)

curl -s -X POST "https://graph.facebook.com/v21.0/1002263869569248/subscribed_apps" \
  -H "Authorization: Bearer $TOKEN"
# → {"success":true}

curl -s "https://graph.facebook.com/v21.0/1002263869569248/subscribed_apps" \
  -H "Authorization: Bearer $TOKEN"
# → {"data":[{"whatsapp_business_api_data":{"name":"Wavefi","id":"1799972834584063"}}]}
```

Meta envoie immédiatement une notification `WEBHOOK_CONFIG_UPDATED` / `subscribed_apps` →
`subscribe`, qui arrive dans `whatsapp_webhook_events`.

### Validation complète, 27/11 à 08h08 (Tahiti)

| Contrôle | Résultat |
|---|---|
| Message entrant reçu | `messages`, expéditeur `68987077019`, HTTP 200 |
| STOP détecté | `system_events` : `whatsapp_stop`, `event_id` `wa-stop:…` |
| Consentement | passé à `false` à 18:08:03 UTC |
| Confirmation envoyée | ✅ sans erreur, et Meta a renvoyé `sent` puis `delivered` |
| Retiré de l'audience | ✅ 0 destinataire sur le lieu après le STOP |

### Les trois leçons

1. **L'envoi et la réception sont deux mécanismes totalement indépendants.** L'envoi passe par le
   jeton ; la réception passe par l'abonnement de l'application au compte. Un système peut envoyer
   parfaitement et ne rien recevoir, sans qu'aucun log ne signale d'erreur.
2. **`subscribed_apps` n'est pas l'abonnement aux champs du webhook.** Le second est visible dans la
   console et rassure ; le premier est invisible et conditionne tout.
3. **Le jeton temporaire de l'étape 1 est un jeton de secours précieux.** Il porte
   `whatsapp_business_management`, il vit 24 heures, et il permet de contourner une interface
   verrouillée pour une opération ponctuelle. À garder en tête pour toute opération administrative
   bloquée par les paramètres de l'entreprise.
