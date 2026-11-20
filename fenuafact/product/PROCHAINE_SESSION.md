# Reprise — prochaine session

> Rédigé le 2026-11-17 à 22h00 (Tahiti). Dernière mise à jour : 2026-11-17, fin de matinée.
>
> **Fait depuis** : application Meta passée en **Live**, pages légales publiées, **Brevo** recréé pour
> `support@fenuafact.com` avec domaine authentifié (DKIM + SPF) — envoi d'email vérifié `delivered`.

## Où on en est

Tout est **en production et fonctionnel** : https://fenuafact.com

- Vocal WhatsApp → devis numéroté → PDF → email client
- Conversion devis → facture (`FAC-2026-0001`)
- API `https://api.fenuafact.com` supervisée toutes les 5 minutes (alerte Discord sur panne API **ou** base)
- Les 5 clés ont été pivotées et les anciennes révoquées

**Rien à faire en urgence.** Si quelque chose tombe cette nuit, l'alerte Discord partira.

## État au 2026-11-19 — produit prêt à recevoir un client

Tout est en production et vérifié : landing page, devis WhatsApp → PDF → email,
factures unifiées avec l'API, relances automatiques (Pro), abonnements Dodo en live
(checkout + montée + descente), webhook Meta signé, base vide et compteurs à zéro.

**Prochain client réel** : il crée son compte, son premier devis sera `DEV-2026-0001`.

### Reste à faire

1. **Renvoi d'appel** `87 04 51 05 → 87 07 70 19` (opérateur) — pour que le numéro business sonne
2. **TAHITI** dès réception (champ `tenants.numero_tahiti`)
3. **Vérification Meta Business** quand la SASU existera
4. **Thème / couleurs** du front (décision esthétique)
5. Points cosmétiques : `fetch` dans abonnement.tsx, `alert` → `toast`

## Historique

## Par quoi commencer demain

### 1. Mode « Live » de l'application Meta 🔴 bloquant

Aujourd'hui seuls les numéros de test peuvent parler au bot. Un vrai artisan ne recevra rien.

- `developers.facebook.com` → app FenuaFact → **Mode de l'application** : basculer de *Développement* à **Live**
- Vérifier le compte business **KaiWeb Marketing** (Business Manager → Sécurité)
- Faire valider le numéro business et les modèles de messages si demandé

**Test de validation** : faire écrire une personne dont le numéro n'est pas dans la liste de test.

### 2. Numéro TAHITI 🟠

Dès réception (SASU KaiWeb Marketing) : à saisir dans les paramètres du front. Sans lui, les factures ne sont pas pleinement conformes. Le champ est actuellement vide, donc rien de faux n'est imprimé.

### 3. Dodo Payments en XPF 🟠

Transaction test de 1 000 XPF avant toute intégration d'abonnement. À vérifier : la devise à zéro décimale.

### 4. GitHub 🟡

Demander à Lovable : « Ce projet est-il connecté à un dépôt GitHub ? Si non, connecte-le. »

### 5. Nettoyage avant la première vraie facture 🟡

Supprimer les documents de test (`DEV-2026-0001`, `DEV-2026-0002`, `FAC-2026-0001`) et remettre les compteurs à zéro, **juste avant** le premier devis réel.

## Rappels personnels du 2026-11-18

1. **Brevo** 🔑 — créer un compte Brevo pour `support@fenuafact.com` (l'actuel est `contact@wavefi.tech`), générer une clé API, la mettre dans `.env` puis redémarrer.
2. **Avocat** ⚖️ — relancer Maître Peuillot (SASU KaiWeb Marketing + numéro TAHITI). *Sujet transversal WaveFi / FenuaFact : sans les statuts de la SASU, aucun des deux projets ne peut se concrétiser.*
3. **Commandant de port** ⚓ — appeler pour demander un rendez-vous (dossier WaveFi).
4. **Tahiti Tourisme** 📣 — contacter la cousine, directrice marketing.

> Un rappel Discord est programmé pour le **2026-11-18 à 04:00 (Tahiti)**, soit 14:00 UTC.
> Tâche one-shot `at` n°1. Vérification : `atq`. Contenu : `ops/rappel_2026-11-18.txt`.

## Détails utiles

| Élément | Valeur |
| --- | --- |
| Front | https://fenuafact.com |
| API | https://api.fenuafact.com |
| Service | `systemctl status fenuafact` |
| Logs | `journalctl -u fenuafact -f` |
| `.env` | `/var/www/fenuafact-api/.env` (600) |
| Supervision | `ops/health.log`, état dans `ops/.health_state` |
| Sauvegarde avant nettoyage | `ops/backups/2026-11-17_avant_nettoyage.json` |

## Points d'attention appris aujourd'hui

- Après `systemctl restart`, attendre 3 s avant de tester (sinon nginx renvoie 502).
- Ne jamais régénérer le **JWT secret** Supabase (casse la connexion du front).
- Meta : « Révoquer les tokens » agit sur **tous** les tokens de l'utilisateur système — révoquer puis générer.
- Le tenant est identifié par le numéro WhatsApp **de l'artisan qui écrit**, pas par le numéro business.
