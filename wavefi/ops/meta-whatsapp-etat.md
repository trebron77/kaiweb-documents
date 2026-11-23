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
