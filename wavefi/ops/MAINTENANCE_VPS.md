# Maintenance du VPS WaveFi — accès, règles, journal

> Ouvert le **21 novembre 2026** (soit le 22/11 en UTC). Concerne le serveur `srv2073733`
> (`31.220.21.53`), qui porte `radius.wavefi.tech`.

## 1. Inventaire du serveur — relevé du 21/11/2026

| Élément | Valeur |
|---|---|
| Système | Ubuntu 26.04.1 LTS, noyau **7.0.0-44-generic** · 2 vCPU |
| RAM | **7,8 Go — 4,7 Go disponibles**, swap à 0 *(montée KVM 2 le 21/11)* |
| Disque | **96 Go — 9,9 Go utilisés, 86 Go libres** (11 %) |
| Services | **tout tourne en Docker** (`docker.service` est le seul service système) |
| Ports exposés | TCP 80 et 443 · **UDP 1812 et 1813** (RADIUS, confirmé en écoute) |
| Mises à jour | 39 appliquées le 21/11, redémarrage effectué ; `unattended-upgrades` **enabled** |

**Conséquence de l'architecture Docker :** `nginx` apparaît « inactive » en service système
— c'est normal, il tourne dans un conteneur. Ne pas s'en alarmer.

## 2. Accès de maintenance

Compte dédié, sans mot de passe, clé `ed25519` (`hotumana@wavefi-ops`).

```bash
ssh -i ~/.ssh/wavefi_vps hotumana@31.220.21.53
```

Droits `sudo` **limités** à : `apt`, `apt-get`, `systemctl`, `reboot`. Vérifié : `cat /etc/shadow`
est refusé. C'est volontaire — le compte ne doit pas pouvoir devenir root en une commande.

⚠️ **Ce qui n'est pas couvert :** Docker. Voir les conteneurs ou les redémarrer demande root, donc
le compte ne peut pas le faire. Deux options si le besoin se présente :
1. `systemctl restart docker` — autorisé, mais brutal : il redémarre toute la pile ;
2. un script root dédié (`/usr/local/bin/wavefi-ops`) avec des sous-commandes fermées
   (`status`, `restart`, `logs <conteneur>`), ajouté au `sudoers`. **À préférer** si les
   interventions deviennent régulières.

## 3. Règles d'intervention

1. **Diagnostiquer avant d'agir.** Lire l'état, puis décider.
2. **Prévenir avant tout redémarrage** — même « rapide ».
3. **Ne rien supprimer** sans accord explicite.
4. **Sauvegarder avant** toute opération qui touche la base ou les volumes.
5. **Consigner ici** chaque intervention : date, commande, résultat.
6. **Ne pas installer** de service qui écoute sur internet sans validation.
7. **Mises à jour de sécurité : automatiques** (`unattended-upgrades`). Redémarrage de noyau :
   dans une fenêtre décidée avec Norbert.

## 4. Journal des interventions

### 2026-11-21 (Tahiti) — mise à niveau initiale

| Action | Résultat |
|---|---|
| `apt update && apt upgrade` (39 paquets) | ✅ appliqués |
| Redémarrage pour charger le noyau 7.0.0-44 | ✅ `uname -r` = 7.0.0-44-generic |
| `systemctl --failed` | ✅ 0 unité en échec |
| `curl -I https://radius.wavefi.tech/admin/login/` | ✅ HTTP/2 200 |
| `unattended-upgrades` | ✅ `enabled` |
| Création du compte `hotumana` + clé + `sudoers` limité | ✅ `visudo -c` : parsed OK |
| Vérification des droits (apt, systemctl autorisés ; `cat /etc/shadow` refusé) | ✅ conforme |
| Inventaire ports / disque / services | ✅ consigné § 1 |

**Effet secondaire mesuré :** la RAM utilisée est passée de 1,7 à 2,4 Go après redémarrage (les
services se chargent complètement). Marge réelle : **1,4 Go** — d'où la décision de passer à 8 Go.

**Point de vigilance :** les 2 mises à jour « ESM Apps » signalées par Ubuntu relèvent d'Ubuntu Pro
(service payant) et ne concernent pas le portail. Sans objet ici.

### 2026-11-21 (Tahiti) — supervision étendue

| Action | Résultat |
|---|---|
| Écriture de `ops/check_vps.py` (contrôle local du serveur) | ✅ |
| Déploiement sur le VPS : `~/wavefi-ops/check_vps.py` | ✅ |
| Webhook Discord dans `~/.wavefi.env` (droits 600) | ✅ |
| Tâche cron `hotumana`, toutes les 6 h | ✅ installée, `cron` actif |
| Test d'envoi Discord (`--heartbeat`) | ✅ message reçu |

**Ce que le script surveille** (et ce que l'ancien contrôle externe ne voyait pas) :

| Contrôle | Seuil d'alerte |
|---|---|
| Disque | > 80 % (critique à 90 %) |
| Mémoire disponible | < 300 Mo (critique < 150 Mo) |
| Swap | > 50 % utilisé (critique à 90 %) |
| Mises à jour en attente | > 20, ou toute mise à jour de sécurité |
| Ports RADIUS 1812/1813 | absents = critique |
| Portail (HTTP 200) | autre code = critique |

**Principe : silence sauf problème.** Le script n'écrit sur Discord que si un seuil est dépassé —
`--heartbeat` force le rapport complet quand on veut un état des lieux.

**Relevé du premier passage :** disque 21 % (37,5 Go libres), mémoire **774 Mo disponibles**
sur 3 911 Mo, swap 0 %, 0 mise à jour, RADIUS en écoute, portail HTTP 200.

⚠️ **774 Mo de marge mémoire : c'est peu.** La valeur oscille entre 0,7 et 1,4 Go selon la charge
des conteneurs. C'est la confirmation chiffrée qu'un palier à 8 Go est nécessaire **avant** le
premier client payant — et qu'aucun contrôleur UniFi ne doit être installé ici.

### 2026-11-21 (Tahiti) — montée à 8 Go (KVM 1 → KVM 2)

| Action | Résultat |
|---|---|
| Snapshot Hostinger avant opération | ✅ (expirait le 22/11) |
| Upgrade de plan depuis hPanel | ✅ facture **H55430228**, 344,71 PLN |
| Redémarrage et migration | ✅ serveur revenu |
| RAM | ✅ **7,8 Go**, dont **4,7 Go disponibles** (contre 764 Mo) |
| Disque | ✅ **96 Go** — agrandi automatiquement, pas de `growpart` nécessaire |
| vCPU | ✅ 2 (contre 1) |
| `systemctl --failed` | ✅ 0 unité en échec |
| Port 3030 (application PM2) | ✅ HTTP 200 |
| Portail `radius.wavefi.tech` | ✅ HTTP 200 |
| RADIUS UDP 1812/1813 | ✅ toujours en écoute |

**Conséquence :** la contrainte mémoire est levée. Le contrôleur UniFi peut désormais être installé
sur ce serveur (1 à 1,5 Go), au lieu d'un portable — c'était l'objectif de la montée en gamme.

⚠️ **Point resté ouvert :** au retrait du module Daily Backup, le crédit Hostinger est passé de
412,37 à 282,19 PLN (−130,18 PLN, ≈ 29 €) sans explication claire. À réclamer sur la base de la
facture H55430228, si le sujet en vaut encore la peine.

### 2026-11-22 (Tahiti) — contrôleur UniFi installé

| Élément | Valeur |
|---|---|
| Image | `jacobalberty/unifi:latest` (UniFi Network v10.0.162) |
| Conteneur | `unifi`, `--restart=always`, réseau hôte |
| Données | `/opt/unifi` (hors conteneur — survit aux mises à jour) |
| Fuseau | `Pacific/Tahiti` |
| Interface | `https://31.220.21.53:8443` |
| Annonce des bornes | `http://31.220.21.53:8080/inform` |
| Ports | 8080, 8443, 8843, 8880, 3478/udp, 10001/udp, 6789, 5514/udp |
| Consommation | ~900 Mo de RAM — il reste 4 Go disponibles |

**Pourquoi cette image :** `lscr.io/linuxserver/unifi-network-controller` a été retirée du registre
(erreur `denied`) et `linuxserver/unifi-controller` est figée depuis janvier 2024. `jacobalberty/unifi`
est la référence maintenue (262 M de téléchargements, mise à jour du 12/12/2025).

⚠️ **Gestion :** le compte `hotumana` n'a pas accès à Docker et ne doit pas l'avoir (le groupe `docker`
équivaut à root). Toute action sur le conteneur — arrêt, mise à jour — se fait depuis la console web
Hostinger, en root :

```bash
docker pull jacobalberty/unifi:latest && docker rm -f unifi && <relancer la commande docker run>
```
