# Chiffrage — plan Entreprise (overlay)

> Rédigé le **2026-11-19** par Hotumana, à la demande du fondateur, qui estime le barème actuel
> (250 000 – 350 000 FCFP) sous-évalué.
> Document **interne** : ne circule jamais tel quel vers un prospect.
> Applicable au PAP/TCI, et réutilisable pour ADT et Air Tahiti Nui.

## 1. Pourquoi le plan Entreprise, et lui seul

| Plan | Limite | Adapté au PAP ? |
|---|---|---|
| Free / Starter / Pro | Commerce indépendant, 1 à 3 lieux | ❌ |
| Business | 10 lieux, **10 000 invités/mois** | ⚠️ suffisant en volume pour le TCI, mais pas d'overlay |
| **Entreprise** | Overlay sur infra existante, SLA, volume élevé | ✅ |

Trois raisons de ne proposer **que** l'Entreprise à une structure comme le PAP :

1. **Overlay technique** : intégration à un contrôleur existant (Cisco, Aruba, Ruckus), pointeur
   RADIUS, tests de charge — ce n'est pas du self-service.
2. **Périmètre multi-sites** : TCI **et** gare maritime. Le TCI génère ~12 100 passagers/mois, dont
   seulement 20 à 40 % se connectent — soit **2 400 à 4 800 invités**, sous le plafond de 10 000 du
   plan Business. La gare maritime, elle, dépasse tout : ~165 000 passagers/mois.
3. **Engagement de service** : un établissement public exige un SLA et un interlocuteur identifié.

### Ce que disent les chiffres officiels du PAP

Source : *Trafic portuaire 2025* du Port autonome de Papeete.

| Périmètre | 2025 | Moyenne mensuelle |
|---|---|---|
| Croisière (TCI) | 145 739 passagers (+34 %) | ~12 100 |
| Cabotage interinsulaire (hors Moorea) | 69 063 | ~5 800 |
| Bornage Tahiti–Moorea (gare maritime) | 1 980 634 | ~165 000 |

**Correction assumée** : j'avais d'abord justifié l'Entreprise par le volume du TCI. Les chiffres
publics ne le confirment pas — même ramené à 10 000 invités, le plafond du plan Business couvre le
TCI, parce qu'une **connexion** n'est pas un **passager** : sur 12 100 passagers mensuels, 2 400 à
4 800 seulement se connectent. L'argument du volume ne tient que si l'on inclut la **gare
maritime**, où il devient écrasant. Ce qui justifie l'Entreprise pour le TCI seul reste l'**overlay**
et le **SLA**, pas le volume.

Et surtout : **volume n'est pas valeur.** Au TCI, le passager est un touriste souvent sans forfait
local, qui attend parfois plusieurs heures : chaque connexion a de la valeur. À la gare maritime,
c'est un résident qui a son forfait et traverse en vingt minutes : le même volume vaut beaucoup
moins. Le TCI est le site vitrine ; la gare maritime est le site à volume.

⚠️ **Le plan Entreprise n'existe pas dans la grille publiée** (Free / Starter / Pro / Business sur
Dodo). Il est décrit dans les notes internes mais **ne peut pas être souscrit aujourd'hui**. À créer
avant toute signature, sinon on ne peut pas encaisser.

## 2. Le barème actuel ne tient pas debout

Le document de référence retient **40 à 60 h** de charge et **7 500 FCFP/h**.

| Calcul | Résultat |
|---|---|
| 40 h × 7 500 | **300 000 FCFP** |
| 60 h × 7 500 | **450 000 FCFP** |
| Fourchette annoncée | 250 000 – 350 000 FCFP |

La fourchette annoncée correspond à **33 à 47 h** au taux retenu — soit **en dessous de la charge
estimée par le document lui-même**. L'incohérence est interne : le prix a été fixé à l'intuition,
pas au calcul. Le fondateur a raison : c'est sous-évalué.

## 3. Décomposition réaliste de la charge

Pour un overlay sur infrastructure publique, avec un DSI en face :

| Phase | Charge | Détail |
|---|---|---|
| Cadrage et réunions techniques | 8 h | 2 réunions + comptes rendus |
| Audit de l'infrastructure | 8 h | contrôleur, VLAN, DHCP/DNS, portail existant |
| Configuration RADIUS + portail | 12 h | SSID, gabarits, langues, tests unitaires |
| Tests d'intégration et de charge | 12 h | pics croisière, montée en invités |
| Recette PAP et corrections | 8 h | allers-retours, anomalies |
| Documentation et passation | 8 h | dossier technique, procédures |
| Cadrage SLA, supervision, alerting | 4 h | engagement de service |
| Marge projet (aléas, attentes) | 8 h | imprévus, délais de disponibilité |
| **Total** | **68 h** | soit ~8,5 jours |

Fourchette prudente : **56 à 72 h**.

## 4. Le prix, au taux du marché polynésien

Taux constatés : 5 000 à 10 000 FCFP/h pour un consultant IT indépendant.

| Taux | 56 h | 72 h | Lecture |
|---|---|---|---|
| 7 500 FCFP/h (taux interne actuel) | 420 000 | 540 000 | plancher défendable |
| 10 000 FCFP/h (expert réseau, face à un DSI) | 560 000 | 720 000 | haut de marché justifiable |

**Recommandation :**

- **Prix affiché (liste) : 480 000 FCFP.**
- **Fourchette de négociation : 400 000 – 550 000.**
- **Plancher absolu sans contrepartie : 300 000 FCFP.**

## 5. L'offre de lancement, si tu veux le site en référence

C'est le seul cas où descendre sous 400 000 se défend — et à une condition : que la remise soit
**visible et contrepartie**.

> « Frais d'intégration : 480 000 FCFP. Dans le cadre de notre premier site de référence, nous
> pouvons les ramener à **300 000 FCFP**, en contrepartie d'une autorisation écrite : citation du PAP
> comme site de référence, étude de cas, et une visite de site pour un prospect. »

Ce que ça change :

| Sans remise affichée | Avec remise affichée |
|---|---|
| 300 000 = ton prix → tu es « le moins cher » | 300 000 = une faveur → tu es « celui qui vaut 480 » |
| Toute négociation future part de 300 | Toute négociation future part de 480 |
| Signal d'amateurisme à un DSI | Signal de maîtrise |

À 250 000, tu ne vends pas un prix : tu annonces que ton travail vaut 3 700 FCFP/h. Un DSI le lit
ainsi, même inconsciemment.

## 6. Le piège du seuil de procédure

Plus le montant monte, plus le dossier risque de basculer dans une **procédure d'achat formalisée**
(publicité, mise en concurrence, délais). Ce n'est pas forcément un mal — mais il faut le savoir
**avant** de chiffrer.

> **À vérifier auprès du service marchés du PAP** : quel seuil déclenche quelle procédure en
> Polynésie française. Aucun chiffre n'est avancé ici : les seuils locaux ne se devinent pas.

Conséquence pratique : demande-leur **le cadre** en même temps que le prix. Un montant qui évite
une procédure de six mois peut valoir une remise ; un montant qui la déclenche doit être assumé.

## 7. L'abonnement Entreprise — à structurer, pas à inventer

Aucun prix récurrent n'existe pour ce plan. Ne pas le fixer avant le pilote : le volume réel
d'invités est inconnu, et c'est lui qui détermine la charge.

Structure proposée :

| Composante | Base de calcul |
|---|---|
| Socle plateforme | forfait mensuel : multi-SSID, gabarits, 3 langues, support prioritaire |
| Palier d'invités | tranches (ex. ≤ 30 000 / ≤ 100 000 / au-delà) |
| Options | marque blanche, hébergement dédié, astreinte, langues supplémentaires |

**Méthode :** mesurer le volume pendant un pilote borné (60 à 90 jours), puis figer le palier.

Les chiffres publics donnent le **plafond théorique** — 12 100 passagers/mois au TCI, 165 000 à la
gare maritime — pas le nombre d'invités : une connexion suppose que le passager sorte son téléphone
et accepte le portail. L'hypothèse de travail est un taux de connexion de **20 à 40 %** : c'est une
hypothèse, pas une donnée. À substituer dès que le PAP communique son taux réel.

Attention aux **pics** : la moyenne mensuelle masque des journées entières à 3 600 ou 4 900
passagers lors d'une seule escale. Le portail doit tenir la pointe, pas la moyenne.

## 8. À faire avant de chiffrer pour le PAP

1. **Créer le plan Entreprise** dans la grille (Dodo + site) — sinon il n'est pas souscriptible.
2. **Vérifier le seuil de procédure** auprès du service marchés.
3. **Ne pas envoyer de devis** avant d'avoir le nombre de points d'accès et le périmètre.
4. **Décider maintenant** si le PAP est le site de référence : la remise en dépend, pas l'inverse.
