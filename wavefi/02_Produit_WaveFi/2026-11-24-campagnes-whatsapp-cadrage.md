# Envoi de campagnes WhatsApp — cadrage

> Décisions du 24/11/2026, avant toute mise en œuvre. À relire avant de modifier ce chantier.

## État des lieux (inventaire Lovable)

| Élément | Constat |
|---|---|
| Écrans | `/campagnes` (liste, filtres, quota, test WhatsApp) et `/campagnes/$id` (détail, 4 compteurs) |
| Canaux | brouillons `email`, `sms`, `whatsapp` — **seul l'e-mail s'envoie** (Brevo) |
| WhatsApp | envoi bloqué client et serveur ; seul le message de test part |
| Données | `campagnes` : 11 lignes (toutes e-mail) · `campagne_livraisons` : 19 lignes e-mail |
| Consentement | forcé en dur côté serveur pour l'e-mail ; **pas forcé pour WhatsApp** côté client |
| Désabonnement | lien signé pour l'e-mail ; **rien pour WhatsApp** |

## Les six décisions

1. **Une seule table de suivi.** `campagne_livraisons` : `email` devient nullable, ajout de
   `telephone` et `canal`. Un vocabulaire unique de statuts. Pas de seconde table — deux tables pour
   la même chose divergent toujours.
2. **Le STOP avant le premier envoi.** Le modèle approuvé promet « Répondez STOP ». Sans traitement
   du message entrant, le désabonnement est une promesse vide et l'envoi se poursuit vers quelqu'un
   qui a refusé. C'est une obligation, pas une option.
3. **Modèles** : lecture des modèles approuvés via l'API, filtre langue `fr`, sélection dans le
   formulaire. En v1, **mapping de variables fixe** par modèle — pas d'éditeur libre.
4. **Consentement forcé côté serveur**, non débrayable par le revendeur, pour les deux canaux.
5. **Blocage Brevo conditionnel au canal** : une campagne WhatsApp ne doit pas dépendre d'une clé e-mail.
6. **Palier Meta** (250 conversations / 24 h au 24/11) et **quota du plan** vérifiés avant envoi, avec
   un message explicite plutôt qu'un échec au milieu de la boucle.

## Ordre de construction

| # | Étape |
|---|---|
| 1 | Schéma de suivi + traitement du STOP |
| 2 | Sélection des destinataires + consentement |
| 3 | Lecture et sélection des modèles approuvés |
| 4 | Boucle d'envoi (Graph API, insertion `whatsapp_messages` avec `is_test = false`) |
| 5 | Écran de suivi par destinataire |

⚠️ La jauge mensuelle de messages ne compte que les envois `is_test = false` — c'est ce que la
campagne devra produire, sinon le quota ne sera jamais consommé et la facturation du dépassement
restera théorique.

## Décision du 24/11 — pas de découverte automatique des modèles

Le jeton Meta porte `whatsapp_business_messaging` (envoi) mais **pas** `whatsapp_business_management`
(découverte des modèles). Or accorder cette permission exige d'accéder aux paramètres Business
Manager, bloqués par un contrôle d'identité envoyé à un ancien numéro (Nouméa, inactif).

**Décision :** le sélecteur de modèles lit la table déclarée `whatsapp-templates.ts` — qui contient
`offre_du_mois` et `demande_avis` avec leur mapping de variables — et **n'interroge plus Meta**.
`listWhatsAppTemplates` reste dans le code, inutilisée et documentée, pour le jour où la permission
sera disponible.

**Pourquoi c'est acceptable :** envoyer un message ne requiert que `whatsapp_business_messaging`,
vérifié fonctionnel (`GET /1437401462784496` → 200, `verified_name: "WaveFi"`). Seule la *découverte*
des modèles exigeait la permission manquante. Un modèle déclaré mais absent produira l'erreur brute de
Meta au moment de l'envoi.

**Conséquence :** ajouter un modèle plus tard demande une ligne de code, pas un appel API.
