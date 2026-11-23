# État de la configuration Meta / WhatsApp — WaveFi

> À remplir le 22/11/2026. Objectif : reconstituer ce qui a déjà été fait avec DeepSeek, afin de
> ne pas recréer ce qui existe. Numéro concerné : **+689 89 63 73 06**.

## 1. Le téléphone

| Question | Réponse |
|---|---|
| Le numéro est-il encore connecté dans l'app WhatsApp Business ? | ................ |
| L'app affiche-t-elle « numéro non disponible » ? | ................ |

> Si le numéro est encore connecté dans l'app → **pas encore migré** vers l'API.
> Si l'app dit « non disponible » → déjà migré, ne pas recommencer.

## 2. Meta Business Manager

| Question | Réponse |
|---|---|
| Une **application Meta** existe-t-elle pour WaveFi ? (nom + ID) | ................ |
| Un **compte WhatsApp Business (WABA)** existe-t-il ? | ................ |
| Le numéro +689 89 63 73 06 y est-il enregistré, avec un `phone_number_id` ? | ................ |
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
