# Runbook — intégrer le portail WaveFi sur une infrastructure existante

> Rédigé le **2026-11-20** par Hotumana pour Norbert Kaimuko.
> Objet : transformer une intégration chez un client (port, aéroport, commerce) en **procédure
> maîtrisée**, au lieu d'une découverte le jour J.
> À lire la veille, à avoir ouvert pendant la réunion.

## 0. La règle d'or

**Tu ne configures jamais seul chez un client.** Tu apportes la méthode, le client apporte l'accès
et la connaissance de son réseau. Une intégration réussie, c'est deux personnes devant le même
écran : son administrateur qui clique, toi qui dictes les valeurs.

Si un client te demande de « faire tout, tout seul, sans lui », c'est un signal : soit il n'a pas
d'administrateur (donc personne pour valider la recette), soit il ne mesure pas ce qu'il demande.

---

## 1. Les huit informations à obtenir avant tout

À demander **par écrit**, avant la réunion technique. Sans elles, tu ne peux pas préparer.

| # | Question | Pourquoi |
|---|---|---|
| 1 | Quel est le **fabricant et le modèle** du contrôleur (ou des bornes si gestion locale) ? | détermine la fiche à appliquer |
| 2 | Quelle **version de firmware** ? | les menus changent, certaines fonctions manquent |
| 3 | Le contrôleur est-il **local, hébergé ou cloud** ? Qui a les droits admin ? | détermine qui clique |
| 4 | Existe-t-il déjà un **SSID invité** ? Quel portail affiche-t-il aujourd'hui ? | évite de casser l'existant |
| 5 | Le réseau invité est-il sur un **VLAN séparé** ? | isolation, responsabilité du client |
| 6 | Le réseau peut-il émettre du **UDP sortant vers 1812/1813** ? | sinon le RADIUS ne passe pas |
| 7 | Y a-t-il un **filtrage sortant** ou un proxy ? | bloque le portail et le walled garden |
| 8 | Qui **signe la recette** ? | désigne la personne qui validera |

**Et une question politique, pas technique :** « si nous devons ouvrir un port UDP sortant, qui
l'autorise et sous quel délai ? » Chez un établissement public, c'est souvent trois semaines.

---

## 2. Le modèle en cinq réglages

Tout contrôleur du marché se configure avec les **mêmes cinq éléments**. Le reste, c'est de l'ergonomie.

| # | Réglage | Valeur WaveFi |
|---|---|---|
| **1** | **Serveur RADIUS** | `radius.wavefi.tech` — **31.220.21.53** · auth UDP 1812, accounting UDP 1813 · secret partagé fourni |
| **2** | **Profil AAA** | le profil qui regroupe le serveur ci-dessus et qui sera référencé par le WLAN invité |
| **3** | **Portail externe** | URL `https://app.wavefi.tech/portail/<client>/login` — hôte **185.158.133.1** |
| **4** | **Walled garden** | `app.wavefi.tech`, `wavefi.tech`, et les domaines CDN utilisés par la page |
| **5** | **SSID invité** | réseau ouvert ou WPA2, isolation VLAN, portail externe activé |

**Le piège numéro un de toutes les intégrations : le walled garden.** Un invité non authentifié n'a
aucun accès internet — donc il ne peut pas charger le portail. Si `app.wavefi.tech` n'est pas dans
la liste blanche, **la page ne s'affiche jamais**. C'est l'erreur qui fait perdre une journée.

---

## 3. Fiche Alcatel-Lucent Enterprise — le cas du PAP

L'infrastructure du TCI est en **Alcatel-Lucent Enterprise**, Wi-Fi 6, avec un SSID invité existant
(`GUEST_TCI`). Trois cas de figure possibles selon la génération.

### 3.1 Gestion par OmniVista 2500 (contrôleur)

Ordre des opérations :

1. **RADIUS** — `Network` → `Unified Access` → `RADIUS Servers` → **Add**
   - Nom : `WaveFi`
   - Adresse IP : celle fournie par WaveFi
   - Port d'authentification : **1812** — port d'accounting : **1813**
   - Secret partagé : celui fourni (à saisir deux fois)
2. **Profil d'authentification** — `Authentication` → `Profiles` → **Add**
   - Serveur primaire : `WaveFi`
   - Type : 802.1X ou MAC selon le mode retenu
3. **WLAN invité** — `Wireless` → `WLANs` → **Add WLAN**
   - SSID : `GUEST_TCI` (conserver l'existant)
   - Sécurité : ouverte avec portail, ou WPA2-Enterprise si 802.1X
4. **Portail captif** — dans les réglages du WLAN, section `Captive Portal`
   - Activer **External Captive Portal**
   - URL de redirection : celle de WaveFi
   - **Walled garden** : ajouter les domaines
5. **Vérification** — `Monitoring` → `RADIUS` : le serveur doit apparaître **connecté**

### 3.2 Gestion par OmniVista Cirrus (cloud)

Même logique, avec le vocabulaire ALE :

- Les serveurs RADIUS se déclarent dans un **AAA server profile**
- Le portail externe et la liste blanche vivent dans un **access role profile**
- Le **WLAN invité** référence ces deux profils
- L'accounting doit être activé avec un **intervalle de 300 secondes** — c'est lui qui alimente les
  statistiques de session

### 3.3 Bornes en mode Instant AP (cluster autonome)

- `Security` → `Authentication Servers` → **Add** : nom, IP, ports, clé partagée
- `Network` → `Networks` → **+** : nom, SSID, type **Guest**
- `Security` : niveau *Enterprise* si 802.1X, sinon réseau ouvert
- `Captive Portal` : sélectionner **External**, saisir l'URL

### 3.4 Ce qui peut bloquer chez le PAP

| Risque | À vérifier au cadrage |
|---|---|
| Version de firmware ancienne | la fonction portail externe peut manquer — demander la version |
| Compte admin délégué | le PAP peut refuser de donner les droits ; prévoir une session partagée |
| Ouverture UDP 1812/1813 | peut nécessiter une demande interne de plusieurs semaines |
| Le SSID `GUEST_TCI` sert déjà à quelque chose | son portail actuel doit être identifié avant de le remplacer |

> Source des chemins de menus : [guide d'intégration Alcatel-Lucent](https://help.ironwifi.com/configuration-guides/other/alcatel-lucent)
> et [guide OmniAccess Stellar](https://www.purple.ai/en-gb/guides/alcatel-lucent-omniaccess-purple-wifi-integration).
> À revérifier selon la version de firmware constatée sur site.

---

## 4. Fiche Ubiquiti UniFi — ton labo

C'est ce que tu utiliseras pour t'entraîner.

1. **Réseau invité** — `Settings` > `Networks` > *Create New* : nom du réseau, VLAN libre, DHCP automatique, option **Network Isolation** activée.
2. **SSID** — `Settings` > `WiFi` > *Create New* : nom, mot de passe vide (réseau ouvert), réseau choisi à l'étape 1, **Application** sur *Hotspot*, **Hotspot Type** sur *Captive Portal*.
3. **Portail** — `Clients` > `Hotspot` > `Landing Page` : activer **External Portal Server**, saisir l'IP du portail, activer **Secure Portal**, renseigner le domaine de redirection.
4. **Walled garden** — `Authorization Access` > `Pre-Authorization Allowances` : ajouter l'IP ou les domaines du portail.
5. **RADIUS** — `Settings` > `Networks` > `RADIUS Servers`, uniquement si authentification 802.1X.

**Attention.** Le contrôleur doit être joignable depuis l'internet si tu utilises le portail externe : IP publique et redirection de port (443 pour un UDM, 8443 pour un contrôleur auto-hébergé). Un contrôleur sur un portable derrière une box ne suffira pas.

## 5. Fiche MikroTik — le kit « petits commerces »

Le plus simple pour un test complet : le hotspot et le client RADIUS sont natifs.

1. `IP` → `Hotspot` → `Server Profiles` : créer un profil (DNS name du portail)
2. `IP` → `Hotspot` → `Servers` : associer le profil à l'interface du réseau invité
3. `RADIUS` : ajouter le serveur (IP, secret), cocher **Hotspot** dans les services
4. `IP` → `Hotspot` → `Walled Garden` : ajouter les domaines du portail
5. `Hotspot` → `User Profiles` : mode *HTTP CHAP* ou *HTTP PAP* selon la configuration du RADIUS

C'est le montage qui te permet de tester **toute la chaîne** pour le prix d'un routeur.

---

## 6. Les autres fabricants — ce qu'il faut chercher

| Fabricant | Où se trouve le réglage | Le piège |
|---|---|---|
| **Ruckus** (SmartZone / Ruckus One) | `RADIUS` puis portail tiers WISPr dans le profil du WLAN | clé d'intégration et domaine de redirection à déclarer |
| **Cisco** (WLC / Catalyst 9800) | `Security` → `RADIUS` → `AAA Servers`, puis *Web Auth* / *External Web Auth* | le portail externe se déclare dans la méthode de sécurité du WLAN |
| **Aruba** (Central / Instant) | profils RADIUS + *External Captive Portal* dans le profil de réseau | les Instant AP gèrent le portail localement, Central le pousse |
| **TP-Link Omada** | `Controller` → `RADIUS Profile` puis portail dans le SSID | fonction portail externe limitée selon les versions |
| **Juniper Mist** | portail externe via API, pas via RADIUS | modèle différent : le portail n'est pas piloté par RADIUS |

Pour ces cinq-là, **ne prépare rien de mémoire** : demande la version de firmware au cadrage et
ouvre la documentation du fabricant la veille.

---

## 7. Le walled garden — la liste à préparer

À donner au client, prête à copier :

| Élément | Valeur |
|---|---|
| Portail | `app.wavefi.tech` |
| Site | `wavefi.tech` |
| API appelée par le portail | à relever dans la console du navigateur |
| Polices et CDN | à relever (souvent un CDN externe) |

**Deux subtilités :**

- Le **RADIUS ne passe pas par le walled garden** : c'est de l'UDP, autorisé par le pare-feu, pas
  par la liste blanche HTTP. Ne confonds pas les deux dans la demande au client.
- La **détection de portail** des téléphones (Apple, Android) interroge des domaines dédiés. Si le
  portail ne répond pas correctement, le téléphone affiche « pas d'internet » alors que la page
  fonctionne. À tester sur un iPhone **et** sur un Android.

---

## 8. La recette — dix vérifications à faire signer

| # | Vérification | Résultat attendu |
|---|---|---|
| 1 | Le SSID invité apparaît | visible sur un téléphone |
| 2 | La connexion déclenche le portail | la page WaveFi s'affiche |
| 3 | Le portail s'affiche sans authentification préalable | walled garden correct |
| 4 | Le formulaire enregistre l'invité | visible dans l'application |
| 5 | Le RADIUS accepte la session | journal RADIUS, `Access-Accept` |
| 6 | L'internet est accordé après validation | navigation possible |
| 7 | La session apparaît en cours | écran « Invités » de l'application |
| 8 | La déconnexion ou l'expiration fonctionne | accès coupé |
| 9 | Rendu correct sur iPhone **et** Android | pas de page blanche |
| 10 | Le client peut refaire le test seul | il a compris où c'était |

La **dixième** est la plus importante : elle te protège le jour où quelque chose tombe et que tu
n'es pas là.

---

## 9. Pannes typiques et diagnostic

| Symptôme | Cause probable | Ce que tu vérifies |
|---|---|---|
| Le portail ne s'affiche jamais | walled garden incomplet | l'URL du portail est-elle joignable depuis le réseau invité ? |
| Page blanche | HTTPS ou certificat | ouvrir l'URL en direct dans le navigateur |
| « Pas d'internet » mais la page marche | détection de portail | tester sur un autre téléphone, vérifier les réponses CNA |
| Le téléphone ne demande rien | SSID encore en WPA2 classique | le portail n'est activé que sur un réseau ouvert ou hotspot |
| `Access-Reject` | secret partagé | comparer caractère par caractère |
| Timeout RADIUS | UDP bloqué | test depuis le contrôleur, pas depuis ton poste |
| Session sans statistiques | accounting désactivé | intervalle 300 s |
| L'invité reste connecté après expiration | session non fermée | vérifier l'accounting *Stop* |

---

## 10. Ce qu'il faut emporter

- Un **téléphone Android** et un **iPhone** — les comportements diffèrent
- Un **câble Ethernet** et un petit switch
- L'accès à la console RADIUS (journaux en direct)
- Le tableau des cinq réglages imprimé
- Les identifiants du contrôleur **si le client les donne** — sinon, il clique

---

## 11. Le jour du PAP, en pratique

1. **Cadrage de 2 heures**, en visio ou sur place, avec l'administrateur réseau du Port.
2. Remplir le tableau du § 1, en séance.
3. Localiser les écrans du § 3 sur **leur** version de firmware, sans rien modifier.
4. Modifier seulement si le client est prêt à tester dans la foulée.
5. Recette du § 8, avec le SSID `GUEST_TCI` **dupliqué** ou sur un SSID de test — jamais sur
   l'existant, pour pouvoir revenir en arrière en une minute.
6. Faire signer la recette.

> **Règle de survie :** ne jamais modifier le SSID `GUEST_TCI` en production sans avoir un SSID de
> test à côté. Une salle d'embarquement sans Wi-Fi, c'est un incident, même cinq minutes.

---

## 12. Sources


- Alcatel-Lucent Enterprise — configuration RADIUS et portail externe :
  https://help.ironwifi.com/configuration-guides/other/alcatel-lucent
- Alcatel-Lucent OmniAccess Stellar (OmniVista Cirrus) — portail externe, profil AAA et access role :
  https://www.purple.ai/en-gb/guides/alcatel-lucent-omniaccess-purple-wifi-integration
- Ubiquiti UniFi — hotspot et portail externe (Network 8 à 10) :
  https://help.ironwifi.com/configuration-guides/ubiquiti/unifi-hotspot

*Chemins de menus relevés au 20 novembre 2026 — à revérifier selon la version de firmware sur site.*

---

## 13. Lexique

Les mots que tu entendras en réunion, et ce que tu en fais.

| Terme | Ce que c'est | Ce que tu en fais |
|---|---|---|
| **SSID** | Nom du réseau Wi-Fi vu par le client | Tu le repères, sans le renommer |
| **Contrôleur** | Le cerveau qui pilote les bornes | Tu y accèdes, ou l'admin ouvre |
| **Portail captif** | La page affichée avant l'accès internet | C'est ta page WaveFi |
| **Splash page** | Synonyme anglais de portail captif | Même chose |
| **RADIUS** | Le service qui répond oui ou non | C'est `radius.wavefi.tech` |
| **1812 / 1813** | Ports d'authentification et de comptabilité | Les deux à ouvrir au pare-feu |
| **Secret partagé** | Mot de passe entre contrôleur et RADIUS | Identique des deux côtés |
| **Access-Accept / Reject** | Les deux réponses du RADIUS | Ce que tu lis dans les journaux |
| **Accounting** | Comptabilité des sessions | Alimente les statistiques (300 s) |
| **Walled garden** | Liste blanche avant authentification | Sans le portail, page invisible |
| **VLAN** | Réseau séparé dans le réseau physique | L'invité ne voit pas l'exploitation |
| **DHCP / DNS** | Distribue les adresses / traduit les noms | S'ils cassent, le portail ne charge pas |
| **UDP** | Transport sans connexion, rapide | C'est ce qu'utilise le RADIUS |
| **802.1X** | Authentification par identifiant | Alternative au portail, pour le personnel |
| **Profil AAA** | Regroupement des serveurs RADIUS | Là où tu déclares WaveFi |
| **Access role profile** | Portail et liste blanche, chez Alcatel Cirrus | Le deuxième objet à configurer |
| **Firmware** | Version du logiciel du contrôleur | À demander avant tout rendez-vous |
