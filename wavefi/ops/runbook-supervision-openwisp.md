# Runbook — supervision OpenWISP

**Rôle :** vérifier chaque jour que l'admin OpenWISP répond, et alerter sur Discord.
**Fichiers :** `ops/check_server.py`, `ops/discord_alert.py`, `ops/discord.env`, journal `ops/check_server.log`.

## Ce qui est vérifié

- URL surveillée : `https://radius.wavefi.tech/admin/login/`
- Critère : réponse **HTTP 200** = en ligne ; tout autre code, timeout, erreur DNS/TLS ou connexion refusée = hors ligne.
- Deux tentatives espacées de 3 s pour éviter un faux positif sur un incident réseau transitoire.

> La racine `https://radius.wavefi.tech/` renvoie **404** (l'application Django n'expose pas de page d'accueil) alors que le service est bien en ligne. C'est pourquoi la vérification cible la page de connexion de l'admin OpenWISP, qui renvoie 200. Pour revenir à la racine : `--url https://radius.wavefi.tech/` (mais l'alerte « hors ligne » partira alors chaque jour).

Messages envoyés (via `ops/discord_alert.py`) :

- En ligne : `✅ [WaveFi] Statut : Serveur OpenWISP en ligne.`
- Hors ligne : `🚨 [WaveFi] ALERTE : Serveur OpenWISP HORS LIGNE.`

## Planification

Le système est en **UTC** et Tahiti est en **UTC-10** toute l'année (pas d'heure d'été) :
**08:00 à Tahiti = 18:00 UTC**.

Ligne installée dans la crontab de `root` :

```cron
# WaveFi — supervision OpenWISP (08:00 heure de Tahiti, UTC-10)
0 18 * * * cd /root/workspace && /usr/bin/python3 ops/check_server.py >> /root/workspace/ops/check_server.log 2>&1
```

> **Depuis le 2026-11-14**, l'espace de travail est passé en multi-projets et `ops/`
> n'existe plus à la racine : c'est un lien symbolique vers
> `projets-clients/wavefi/ops/`. La ligne ci-dessus reste donc valide. Cible à
> appliquer lors de la prochaine intervention sur la crontab :
>
> ```cron
> 0 18 * * * cd /root/workspace && /usr/bin/python3 projets-clients/wavefi/ops/check_server.py >> /root/workspace/projets-clients/wavefi/ops/check_server.log 2>&1
> ```

## Vérifier que la tâche est enregistrée

```bash
crontab -l | grep -A1 -B1 check_server   # la ligne doit apparaître
systemctl status cron --no-pager         # doit être « active (running) »
```

Vérifier le script tout de suite, sans envoyer de message :

```bash
python3 ops/check_server.py --dry-run
```

Simuler l'environnement minimal de cron (locale C, pas de variables) :

```bash
env -i PATH=/usr/bin:/bin LANG=C /bin/sh -c \
  'cd /root/workspace && /usr/bin/python3 ops/check_server.py --dry-run'
```

Après la première exécution de 08:00, contrôler le journal :

```bash
tail -n 5 ops/check_server.log
```

## Codes de sortie

| Code | Signification |
| --- | --- |
| `0` | Serveur en ligne, alerte envoyée |
| `1` | Serveur hors ligne, alerte envoyée |
| `2` | Alerte non délivrée (échec de `discord_alert.py`) |
| `3` | Erreur d'exécution (option invalide, script d'alerte introuvable) |

## Modifier la surveillance

- Changer d'URL ponctuellement : `python3 ops/check_server.py --url https://...`
- Changer durablement : modifier la ligne cron et/ou la constante `DEFAULT_URL`.
- Changer l'heure : recalculer l'heure UTC correspondante, puis `crontab -e`.
- Tester un envoi réel immédiat : `python3 ops/check_server.py`.
