# Commandes techniques — mode d'emploi

> **Pour Norbert.** Chaque procédure est écrite ici, une fois. Si une commande est nécessaire,
> elle est dans ce fichier — inutile de la redemander à Hotumana.
> Dernière mise à jour : 28 novembre 2026.

## Règle d'or : UNE commande à la fois

La console web de Hostinger **abîme les collages multi-lignes**. Une commande collée avec d'autres
peut être exécutée à moitié, ou pas du tout.

**Toujours** : coller une seule ligne → appuyer sur **Entrée** → lire le résultat → passer à la
suivante. Jamais plusieurs à la fois, jamais avec les commentaires `#`.

## 1. Se connecter au serveur

Hostinger → VPS → **Terminal** (`phx.hostingvps.com/1213`). L'invite doit afficher :

```
root@srv2073733:~#
```

## 2. Vérifier qu'une route protégée est vraiment protégée

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://app.wavefi.tech/api/public/cron/surveillance-whatsapp
```
Attendu : **401** *(aucun en-tête fourni → refusé)*

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://app.wavefi.tech/api/public/cron/surveillance-whatsapp -H "Authorization: Bearer faux-secret"
```
Attendu : **401** *(mauvais secret → refusé)*

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://app.wavefi.tech/api/public/cron/surveillance-whatsapp
```
Attendu : **401** ou **405** — **jamais 200**

## 3. Déclencher la surveillance WhatsApp à la main

Remplacer `TON_SECRET` par la valeur de `LOVABLE_CRON_SECRET` :

```bash
curl -s -X POST https://app.wavefi.tech/api/public/cron/surveillance-whatsapp -H "Authorization: Bearer TON_SECRET" -H "Content-Type: application/json" -d '{}'
```
Attendu : un JSON avec trois compteurs. Aucune alerte si tout va bien.

## 4. Rattacher une application Meta à un compte WhatsApp

Remplacer `TON_JETON` par un jeton généré depuis « Étape 1. Faites un essai » (valable 24 h) :

```bash
TOKEN="TON_JETON"
```

```bash
curl -s "https://graph.facebook.com/v21.0/1002263869569248?fields=id,name" -H "Authorization: Bearer $TOKEN"
```
Attendu : `{"id":"1002263869569248","name":"WaveFi"}`

```bash
curl -s -X POST "https://graph.facebook.com/v21.0/1002263869569248/subscribed_apps" -H "Authorization: Bearer $TOKEN"
```
Attendu : `{"success":true}`

```bash
curl -s "https://graph.facebook.com/v21.0/1002263869569248/subscribed_apps" -H "Authorization: Bearer $TOKEN"
```
Attendu : la liste des applications abonnées, dont `Wavefi`.

## 5. Où sont les secrets

Lovable → projet → **Secrets**. Attention : les valeurs sont **en écriture seule** — une fois
enregistrées, elles ne peuvent plus être relues. Il faut donc les **noter au moment de la création**,
dans un gestionnaire de mots de passe. Jamais dans ce dépôt, jamais dans un document.

## Règles de travail avec Hotumana

| Règle | Pourquoi |
|---|---|
| **Une commande à la fois**, avec le résultat attendu | la console abîme les collages |
| Un prompt Lovable = **tout dedans**, y compris ce qu'on veut en retour | sinon il faut un second envoi |
| Toujours dire **dans quel projet** (app ou vitrine) | ce sont deux dépôts séparés |
| Toujours dire **où c'est écrit** (fichier, ligne) | pour retrouver sans redemander |
| Pas de méthode longue quand une phrase suffit | Norbert ne « pianote » pas à la vitesse d'un agent |
| Vérifier **sur l'URL en ligne**, jamais dans l'aperçu | enregistré ≠ publié |
