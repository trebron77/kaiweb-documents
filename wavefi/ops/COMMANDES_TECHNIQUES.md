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

## 1 bis. ATTENTION — le VPS ne peut pas joindre app.wavefi.tech

Constaté le 28/11/2026 : depuis le VPS, toute requête vers `app.wavefi.tech` renvoie **`000`**
après 20 secondes. Le DNS résout (185.158.133.1) mais la **connexion TCP 443 est filtrée** :
l'hébergeur du site refuse les adresses de datacenter. `graph.facebook.com`, lui, répond
normalement — le problème est propre à cet hébergement.

**Conséquence : les tests vers `app.wavefi.tech` se font depuis le PC de Norbert, en PowerShell.**
Les tâches planifiées, elles, sont appelées par Lovable depuis son propre réseau : elles ne sont
pas concernées.

## 2. Vérifier qu'une route protégée est vraiment protégée

**Depuis PowerShell (Windows)** — `curl.exe`, avec l'extension, sinon PowerShell appelle un autre
programme :

```powershell
curl.exe -s -o NUL -w "%{http_code}" -X POST https://app.wavefi.tech/api/public/cron/surveillance-whatsapp
```

*(Depuis un serveur Linux joignable :)*

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

## 3. Déclencher la surveillance WhatsApp à la main — IMPOSSIBLE, et c'est normal

`LOVABLE_CRON_SECRET` porte le préfixe réservé `LOVABLE_` : ce secret est **créé et géré par
Lovable**, injecté automatiquement dans les tâches planifiées, et **invisible** dans la liste des
secrets du projet. On ne peut donc pas le connaître, et l'appel manuel renverra toujours `401`.

Ce n'est pas une panne : la tâche s'exécute côté Lovable, à l'heure prévue.

**Comment vérifier qu'elle tourne :** lire la table `system_events` et y chercher un événement
`surveillance_executee` portant les trois compteurs. C'est la trace demandée à Lovable le 28/11.

*(Procédure conservée ci-dessous pour mémoire, si un jour le secret devenait accessible.)*

### Ancienne procédure

Remplacer `TON_SECRET` par la valeur de `LOVABLE_CRON_SECRET` — **depuis PowerShell** :

```powershell
curl.exe -s -X POST https://app.wavefi.tech/api/public/cron/surveillance-whatsapp -H "Authorization: Bearer TON_SECRET" -H "Content-Type: application/json" -d '{}'
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
