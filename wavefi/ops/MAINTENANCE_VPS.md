# Maintenance du VPS WaveFi — accès, règles, journal

> Ouvert le **21 novembre 2026** (soit le 22/11 en UTC). Concerne le serveur `srv2073733`
> (`31.220.21.53`), qui porte `radius.wavefi.tech`.

## 1. Inventaire du serveur — relevé du 21/11/2026

| Élément | Valeur |
|---|---|
| Système | Ubuntu 26.04.1 LTS, noyau **7.0.0-44-generic** |
| RAM | 3,8 Go — **1,4 Go disponibles**, swap à 0 |
| Disque | 48 Go — **9,9 Go utilisés, 38 Go libres** (21 %) |
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
services se chargent complètement). Marge réelle : **1,4 Go**. Cela confirme qu'aucun contrôleur
UniFi ne doit être installé sur cette machine — il lui faut 1 à 1,5 Go à lui seul.

**Point de vigilance :** les 2 mises à jour « ESM Apps » signalées par Ubuntu relèvent d'Ubuntu Pro
(service payant) et ne concernent pas le portail. Sans objet ici.
