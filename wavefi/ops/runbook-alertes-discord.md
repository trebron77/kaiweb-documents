# Runbook — alertes Discord

**Rôle :** envoyer une alerte d'exploitation (supervision, sauvegarde, incident) sur un salon Discord de WaveFi.
**Fichier :** `ops/discord_alert.py` — dépendance : Python 3.9+ uniquement (bibliothèque standard).

## 1. Créer le webhook Discord

1. Dans Discord, ouvrir le salon cible → **Paramètres du salon** → **Intégrations** → **Webhooks**.
2. **Nouveau webhook**, choisir le nom (ex. « WaveFi Alertes ») et le salon.
3. **Copier l'URL du webhook** (elle ressemble à `https://discord.com/api/webhooks/<id>/<token>`).

L'URL du webhook est un secret : toute personne qui la possède peut publier dans le salon.

## 2. Renseigner l'URL

Coller l'URL dans `ops/discord.env`, ligne `DISCORD_WEBHOOK_URL=` :

```dotenv
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_ALERT_USERNAME=WaveFi Alertes
```

Vérifier les droits : `chmod 600 ops/discord.env`.

Le fichier est exclu par `ops/.gitignore`. Pour rester conforme à la règle du
`README.md` (« ne jamais stocker de secret dans `ops/` »), la méthode
recommandée en production est une variable d'environnement alimentée par le
gestionnaire de secrets :

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

Ordre de priorité : `--webhook` > `DISCORD_WEBHOOK_URL` > `ops/discord.env`.
Un autre fichier peut être indiqué avec `--config` ou `DISCORD_ALERT_CONFIG`.

## 3. Tester

```bash
# Vérifie la configuration sans rien envoyer
python3 ops/discord_alert.py --dry-run "Test de configuration"

# Envoi réel
python3 ops/discord_alert.py "✅ Test alerte Discord"
```

Attendu : `Alerte Discord envoyée.` et le message dans le salon.

## 4. Utiliser

```bash
# Message simple
python3 ops/discord_alert.py "Sauvegarde terminée"

# Depuis un pipe
df -h / | tail -1 | python3 ops/discord_alert.py

# Depuis cron (toutes les 5 minutes)
*/5 * * * * /usr/bin/python3 /root/workspace/projets-clients/wavefi/ops/discord_alert.py --quiet \
  "❌ API injoignable" >/dev/null 2>&1
```

Le message est limité à 2 000 caractères (tronqué au-delà). Les mentions
`@everyone`/`@here` sont neutralisées (`allowed_mentions.parse = []`).

## 5. Codes de sortie

| Code | Signification |
| --- | --- |
| `0` | Alerte envoyée (ou `--dry-run` valide) |
| `1` | Usage invalide (message vide, option incorrecte) |
| `2` | Configuration absente ou URL refusée |
| `3` | Discord a répondu une erreur HTTP (après reprise sur 429/5xx) |
| `4` | Webhook injoignable (réseau, DNS, timeout) |

## 6. Sécurité et dépannage

- Ne jamais coller l'URL dans un ticket, un journal ou un commit.
- En cas de fuite : supprimer le webhook dans Discord, en créer un nouveau, mettre à jour la configuration.
- `Hôte non autorisé` : l'URL doit être un webhook `discord.com` en `https://` ; le script refuse tout autre hôte pour éviter d'envoyer le message ailleurs.
- `HTTP 401/404` : webhook supprimé ou URL incomplète — en générer une nouvelle.
- `HTTP 429` : limite de débit Discord ; le script attend puis réessaie (3 tentatives).
