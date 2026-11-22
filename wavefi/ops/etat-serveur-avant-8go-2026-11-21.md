# État du serveur avant la montée à 8 Go — 2026-11-21

> Relevé fait **avant** le changement de plan Hostinger (KVM 1 → KVM 2), pour pouvoir vérifier
> après coup que tout est revenu, et savoir à quoi revenir en cas de problème.

## 1. État de référence

| Élément | Valeur |
|---|---|
| Relevé (UTC) | 2026-11-22T07:22:16Z — soit **21/11 21h22 à Tahiti** |
| Système | Ubuntu 26.04.1 LTS |
| Noyau | 7.0.0-44-generic |
| RAM | **3 911 Mo** au total, **764 Mo** disponibles |
| Swap | 2 047 Mo, 0 utilisé |
| Disque | 48 Go — 9,9 Go utilisés, **38 Go libres** |
| Paquets installés | 658 |
| Portail externe | HTTP 200 |
| Application locale `:3030` | HTTP 200 |

## 2. Ce qui tourne — à retrouver à l'identique après

| Élément | Détail |
|---|---|
| `docker.service` | **actif** — la pile portail/RADIUS tourne en conteneurs |
| `pm2-root.service` | **actif** — gère une application Node (Express + React) sur le port **3030** |
| Ports TCP | 22 (SSH), 80, 443, **3030**, 65529 (localhost) |
| Ports UDP | **1812** (RADIUS auth), 1813 (RADIUS accounting), 1194 |
| `cron.service` | actif — porte la tâche `check_vps.py` toutes les 6 h |
| `monarx-agent` | agent de sécurité de l'hébergeur |
| Autres | chrony, containerd, dbus, rsyslog, ssh, unattended-upgrades, qemu-guest-agent |

> **Nombre de conteneurs Docker : indéterminé** — le compte `hotumana` n'a pas accès au démon Docker.
> À vérifier après la migration, depuis la console root (`docker ps`).

## 3. À vérifier après la migration

```bash
free -h                      # ~8 Go attendus
df -h /                      # disque agrandi (100 Go) ou non
uname -r                     # 7.0.0-44-generic
systemctl --failed           # vide
curl -I http://127.0.0.1:3030/          # 200 — application PM2
curl -I https://radius.wavefi.tech/admin/login/   # 200 — portail
ss -lun | grep -E '1812|1813'           # RADIUS toujours en écoute
crontab -l                   # tâche check_vps présente
docker ps                    # depuis root : conteneurs remontés
```

Puis, depuis ici : `python3 ops/check_vps.py --dry-run` sur le VPS — les six contrôles doivent être
au vert, et la mémoire disponible doit dépasser **4 Go**.

## 4. Si le disque n'est pas agrandi

La migration peut laisser le système de fichiers à 48 Go alors que le disque en fait 100. Deux
commandes, **en root dans la console web** :

```bash
growpart /dev/sda 1
resize2fs /dev/sda1
```

Le compte `hotumana` ne peut pas les exécuter (hors périmètre sudo). À faire depuis la console.

## 5. Retour arrière

Un **snapshot Hostinger** est pris avant l'opération. En cas de problème : hPanel → VPS →
Snapshots → restaurer. C'est la raison d'être de ce document : savoir ce qu'on doit retrouver.
