# Fiche technique — Portail Wi-Fi d'accueil du TCI

| | |
|---|---|
| **Destinataire** | Service informatique du Port Autonome de Papeete |
| **Émetteur** | Norbert Kaimuko — WaveFi (KaiWeb Marketing) |
| **Version** | 1.0 — 19/11/2026 |
| **Objet** | Décrire le fonctionnement, les prérequis et les limites du portail d'accueil WaveFi, pour permettre à vos équipes d'évaluer sa faisabilité sur l'infrastructure du TCI. |

> Ce document décrit uniquement le dispositif technique. Il ne contient ni engagement commercial,
> ni prix : ces éléments relèvent d'une proposition séparée. Les points marqués **« à valider »** sont
> volontairement laissés ouverts : ils dépendent de votre infrastructure et de vos règles internes.

---

## 1. Le principe : overlay, sans remplacement

WaveFi ne fournit pas de matériel, ne remplace ni l'opérateur, ni le contrôleur, ni le fournisseur
d'accès. Le dispositif s'ajoute à l'installation existante : il prend en charge la **page d'accueil**
que voit le passager au moment où il se connecte au réseau invité.

```text
  Passager
     │  association au SSID invité (existant)
     ▼
  Borne / contrôleur du PAP ──────────────► DHCP / DNS (existants)
     │
     │  requête d'authentification (RADIUS)
     ▼
  radius.wavefi.tech ──► page d'accueil personnalisée (portail)
                              │
                              ▼
                    contenus, langues, statistiques agrégées
```

Trois conséquences concrètes :

1. **Aucun câblage, aucune borne, aucun routeur à installer.**
2. **Aucun changement d'opérateur ni de prestataire réseau.**
3. **Le réseau d'exploitation du port n'est jamais concerné** : seul le SSID invité est en jeu.

## 2. Ce que le dispositif ne fait pas

Le périmètre exclu est aussi important que le périmètre inclus — il évite les malentendus.

| Exclu | Précision |
|---|---|
| Sûreté portuaire, contrôle d'accès | WaveFi ne contrôle personne et ne se substitue à aucun dispositif de sûreté. |
| Vidéosurveillance | Aucun lien, aucune caméra. |
| Filtrage de contenu | Reste du ressort du contrôleur ou de la politique du PAP. |
| Accès aux systèmes d'information du port | Le portail n'accède à aucun SI interne. |
| Remplacement du portail existant | Si un portail existe déjà, il est remplacé **ou** complété, au choix du PAP. |

## 3. Composants

| Composant | Rôle | Hébergement |
|---|---|---|
| Portail captif | Page d'accueil, consentement, informations passagers | WaveFi (cloud) |
| Service d'authentification RADIUS | Identification des invités, autorisation de session | WaveFi — `radius.wavefi.tech` |
| Console d'administration | Gabarits, contenus, langues, statistiques | WaveFi |
| Supervision | Contrôle de disponibilité et alerte | WaveFi |

Aucun de ces composants ne s'exécute sur le réseau du PAP.

## 4. Prérequis côté PAP

| # | Prérequis | Détail |
|---|---|---|
| 1 | **SSID invité** | **Déjà en place : `GUEST_TCI`** — à conserver tel quel. Reste à vérifier l'isolation VLAN avec votre équipe réseau |
| 2 | **DHCP et DNS** sur le réseau invité | Fournis par l'infrastructure existante |
| 3 | **Accès sortant RADIUS** | UDP 1812/1813 vers `radius.wavefi.tech` (ou 1645/1646 selon configuration) : **port à ouvrir par vos équipes** |
| 4 | **HTTPS sortant** | Pour l'affichage du portail et de ses contenus |
| 5 | **Un interlocuteur technique** | Pour la configuration du contrôleur et la recette |
| 6 | **Adresse d'expédition** *(facultatif)* | Pour les e-mails éventuels au nom du PAP |

## 5. Matériel et contrôleurs

Le TCI est équipé en **Alcatel-Lucent Enterprise**, en **Wi-Fi 6 (802.11ax)** — relevé NetAnalyzer
de la campagne terrain WaveFi, confirmé par un relevé radio sur site le 19/11/2026.

**Un SSID invité existe déjà : `GUEST_TCI`.** Le projet ne consiste donc pas à créer un réseau
invité, mais à en changer le portail d'accueil : le SSID, le VLAN et l'adressage restent en place.

Ces équipements de génération Wi-Fi 6 disposent des fonctions requises — redirection vers un portail
externe et authentification auprès d'un service RADIUS externe. Le paramétrage précis (profil
d'authentification, règle de redirection, gabarit du portail) sera arrêté avec vos équipes lors du
cadrage : c'est un travail de configuration, pas un changement d'équipement.

À titre indicatif, les environnements déjà relevés sur le territoire sont majoritairement Ruckus
Wireless, Cisco Systems, Ubiquiti, Hewlett Packard Enterprise et Edgecore. La compatibilité ne dépend
pas de la marque, mais de deux capacités du contrôleur : pointer vers un RADIUS externe et afficher
un portail externe.

## 6. Données personnelles

| Sujet | Position |
|---|---|
| Données collectées | E-mail et/ou téléphone **si le passager les saisit** ; sinon données de session |
| Base | **Consentement explicite** à la connexion, finalité affichée sur la page d'accueil |
| Statistiques | **Agrégées et anonymisées** : affluence, pics, langues, rubriques consultées |
| Revente | **Aucune** |
| Conservation | **À définir avec le PAP** — nous appliquons la durée que vous fixez |
| Sous-traitants | Hébergement cloud et e-mailing ; liste détaillée fournie dans une annexe DPA |
| Gouvernance | Le PAP reste **responsable des finalités** ; nous sommes sous-traitant |

## 7. Sécurité

- Échanges en **HTTPS** entre le passager et le portail.
- L'isolation du réseau invité relève de l'architecture du PAP (VLAN) — c'est le point de sécurité
  principal, et il est déjà de votre responsabilité.
- Le portail n'a **aucun accès** aux systèmes d'information du port.
- Comptes d'administration : à cadrer avec vous (comptes nominatifs, authentification forte).
- Journalisation : **à préciser** selon vos exigences.

## 8. Supervision et disponibilité

- Un contrôle de disponibilité du portail est déjà en place, avec alerte quotidienne.
- **Aucun SLA contractuel n'existe à ce jour.** Si le projet se poursuit, un engagement de service
  est à définir conjointement — c'est l'un des objets de la phase de cadrage.

## 9. Mise en œuvre envisagée

| Phase | Charge | Qui |
|---|---|---|
| Cadrage et réunion technique | 1 réunion | PAP + WaveFi |
| Analyse de l'infrastructure existante | 1 à 2 jours | WaveFi, sur documents fournis |
| Configuration du portail et du RADIUS | 2 à 3 jours | WaveFi |
| Tests d'intégration | 1 à 2 jours | PAP + WaveFi |
| Recette | 1 jour | PAP |
| Documentation et passation | 1 jour | WaveFi |

**Durée indicative : 1 à 2 semaines**, hors délais de disponibilité des interlocuteurs.

## 10. Dimensionnement — données publiques du PAP

Les volumes ci-dessous sont issus du *Trafic portuaire 2025* publié par le Port autonome de Papeete.
Ils servent à cadrer la capacité du portail, pas à présumer du taux de connexion réel.

| Périmètre | 2025 | Ordre de grandeur mensuel |
|---|---|---|
| **Croisière** (escales à Papeete) | **145 739 passagers** (+34 % sur 2024) | ~12 100 / mois |
| — dont transpacifique | 132 029 | |
| — dont interinsulaire | 13 710 | |
| **Cabotage interinsulaire** (hors Moorea) | 69 063 passagers | ~5 800 / mois |
| **Bornage Tahiti–Moorea** | **1 980 634 passagers** | ~165 000 / mois |

Escales 2025 : 180 au total (132 transpacifique, 48 interinsulaire). Plus grands navires observés :
*Anthem of the Seas* (4 900 passagers) et *Crown Princess* (3 600).

**Lecture :** le TCI est un site à **forte valeur** — passagers internationaux, souvent sans forfait
local, en attente prolongée. La gare maritime est un site à **fort volume** — navettes Moorea, trafic
quotidien de résidents. Le dimensionnement dépend donc du **taux de connexion** que vous observez,
pas du trafic total : c'est le seul chiffre qui nous manque pour calibrer l'offre.

> Source : *Trafic portuaire 2025*, Port autonome de Papeete —
> https://www.portdepapeete.pf/wp-content/uploads/2026/07/Trafic-portuaire-2025.pdf

## 11. Points à valider ensemble

1. **Mode de gestion du Wi-Fi** : contrôleur local ou gestion cloud, et accès administrateur
   nécessaire pour configurer le profil d'authentification.
2. **Portail actuel** : existe-t-il ? qui l'exploite ? que doit-il devenir ?
3. **Taux de connexion** : part des passagers qui se connectent au Wi-Fi invité aujourd'hui, si un
   SSID existe. C'est ce chiffre — et non le trafic total — qui dimensionne l'abonnement.
4. **Conservation des données** : durée et règles internes du PAP.
5. **Hébergement** : exigences éventuelles de localisation des données.
6. **Cadre d'achat** : pilote, ou procédure formalisée — votre service achats tranche.

---

**Contact technique** — Norbert Kaimuko · contact@wavefi.tech · +689 87 70 01 79
WaveFi — solution de Wi-Fi marketing validée par la DGEN (Direction générale de l'économie numérique).

<!-- pagebreak -->

## Annexe A — Glossaire

Les termes ci-dessous sont employés dans le présent document **au sens suivant**. Ils précisent
l'usage retenu, et non la définition générale de ces notions.

| Terme | Sens retenu dans ce document |
|---|---|
| **Overlay** | Mode de déploiement dans lequel la solution s'ajoute au réseau existant sans le remplacer : aucun matériel fourni, aucun changement d'exploitant. |
| **Réseau invité** | Le réseau Wi-Fi destiné aux passagers, distinct du réseau d'exploitation. Au TCI : SSID `GUEST_TCI`. |
| **Portail d'accueil** | La page présentée au passager au moment de la connexion, avant l'ouverture de l'accès internet. |
| **Invité** | Un appareil ayant ouvert une session sur le portail. C'est l'unité de décompte des quotas. |
| **Session** | La période comprise entre l'authentification d'un invité et sa déconnexion ou son expiration. |
| **Liste d'autorisation** *(walled garden)* | Les adresses joignables avant authentification, limitées au nécessaire au fonctionnement du portail. |
| **Indicateurs agrégés** | Données de fréquentation restituées sous forme de totaux — affluence, pics, langues — sans identification des personnes. |
| **Sous-traitant** | WaveFi, qui traite les données pour le compte du PAP, responsable du traitement. |
| **Annexe de traitement** *(DPA)* | Document encadrant les finalités, les durées et les garanties du traitement des données. |
| **Prestation d'intégration** | Les travaux de mise en service, facturés une fois, distincts de l'abonnement. |
| **Recette** | La vérification contradictoire des points de contrôle, qui vaut acceptation du dispositif. |
| **Niveau de service** *(SLA)* | Les engagements de disponibilité et de délai de prise en charge, définis par contrat. |

*Ce glossaire ne définit pas les notions générales de réseau — adressage, VLAN, protocoles —
supposées connues du service destinataire.*
