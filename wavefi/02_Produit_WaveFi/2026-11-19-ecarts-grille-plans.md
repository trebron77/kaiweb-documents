# Écarts entre la grille produit et les documents contractuels

> Constat établi le **2026-11-19** par Hotumana, à la demande du fondateur (« les plans ont été
> mis à jour, le plan Business est passé à 15 000 invités/mois »).
> Objet : il existe **quatre versions différentes** de la même grille. Aucune n'est fausse — elles
> ont simplement divergé. Tant qu'aucun client n'a signé, c'est le bon moment pour n'en garder
> qu'une.

## 1. Les quatre sources

| Source | Free | Starter | Pro | Business | Enterprise |
|---|---|---|---|---|---|
| **CGV v1.3** (en vigueur 11/10/2026) | 1 lieu / 50 | **3 lieux** / 1 000 | **10 lieux / 20 000** | **20 lieux / 100 000** | Illimité |
| **Annexe 5 SLA v1.1** | — | — | — | **100 000 invités/mois** | **Illimité** |
| **Grille produit (Dodo)** | 1 / 50 | 1 / 1 000 | 3 / 5 000 | 10 / 30 000 | *absent* |
| **Annonce du 19/11** | 1 / 50 | 1 / 1 000 | 3 / 5 000 | **10 / 15 000** | *absent* |

## 2. Le problème, en une phrase

**Le contrat et le back-end annoncent 100 000 invités ; la vitrine commerciale en affiche 30 000.**

En vérifiant le journal de build, on trouve la jauge réelle du dashboard : « Lieux 2/20, Invités
0/100 000 ». Le back-end applique donc **20 lieux et 100 000 invités** au plan Business — exactement
ce que dit la CGV. C'est la grille commerciale (Dodo, site) qui était en retard à 10 lieux et
30 000 invités.

Conséquence : il n'y a pas, aujourd'hui, de client lésé par un plafond. Mais la décision du 19/11 de
passer Business à **10 000 invités** crée un écart **inverse** : c'est désormais le contrat qui
promet plus que ce que le produit accordera. D'où la CGV v1.4.

Règle à retenir : **le contrat ne doit jamais promettre plus que le back-end.** Promettre moins et
livrer plus est la seule posture tenable avant le premier client.

## 3. Un second angle : les critères de classement

La CGV classe les plans par **effectif et chiffre d'affaires** :

| Plan | Critère |
|---|---|
| Starter | moins de 10 salariés, CA < 50 M XPF |
| Pro | 10-50 salariés, CA < 200 M XPF |
| Business | 50-200 salariés, CA < 1 Md XPF |
| Enterprise | plus de 200 salariés ou CA > 1 Md XPF |

Pour un **établissement public** comme le Port Autonome, ces critères ne s'appliquent pas : un port
n'a pas de chiffre d'affaires au sens commercial, et son effectif le placerait mécaniquement en
Enterprise. Le PAP n'est donc pas « un client Business » : c'est un cas **Enterprise par nature**,
avec un contrat d'intégration (overlay), pas un abonnement de grille.

## 4. Bonne nouvelle : Enterprise existe déjà

Contrairement à ce que j'avais écrit le 19/11, **le plan Enterprise n'est pas à inventer** : il
figure déjà dans les CGV v1.3 (illimité) et dans l'annexe SLA v1.1 (illimité, 10 000 utilisateurs
simultanés, 1 000 requêtes/seconde).

Il manque seulement dans le **parcours d'achat**. C'est un travail de configuration, pas de
rédaction juridique.

## 5. Ce que les CGV permettent de modifier

| Clause | Portée | Délai |
|---|---|---|
| **Art. 4.3 — Révision des prix** | Modifier les **tarifs** | Préavis **60 jours** ; le client peut résilier |
| **Art. 12 — Modification des CGU/CGV** | Modifier **le texte**, donc les quotas | Préavis **30 jours** ; résiliation sans frais possible |
| **Plan Free** | Modifier ou supprimer le plan | Préavis **60 jours** |

Conclusion : **baisser un quota est juridiquement possible, mais coûteux** — 30 jours de préavis, et
le client peut partir sans frais. Ce n'est pas une ligne à changer dans un tableau : c'est une
renégociation. À faire **avant** toute signature, jamais après.

## 6. Recommandation

**Une seule source de vérité : la grille produit.** On aligne les CGV vers le bas, sur ce que
l'application sait réellement faire. Promettre moins et livrer plus est la seule posture tenable
pour une société qui n'a pas encore de client.

| Plan | Valeur à retenir | Justification |
|---|---|---|
| Free | 1 lieu / 50 | inchangé |
| Starter | 1 lieu / 1 000 | le produit ne gère qu'un lieu aujourd'hui |
| Pro | 3 lieux / **3 000** | **décidé le 19/11** — inchangé |
| Business | 10 lieux / **10 000** | **décidé le 19/11** |
| **Enterprise** | **Illimité, sur devis** | à activer dans le parcours d'achat |

Puis, dans l'ordre : mettre à jour la CGV v1.3 → **v1.4**, l'annexe 5 SLA, la page tarifs du site,
et la fiche produit.

## 7. Décision du 19/11

| Point | Décision |
|---|---|
| Business | **10 000 invités/mois** |
| Pro | **3 000 invités/mois** — inchangé |
| Starter | 1 000 — inchangé |
| Enterprise | illimité, sur devis |

**Reste à trancher : les « lieux ».** La CGV dit 1 / 3 / 10 / 20 ; la vitrine dit 1 / 1 / 3 / 10 ;
le back-end applique 20 au Business. Aucune de ces trois colonnes ne concorde.

Le plan d'exécution complet — documents légaux, back-end, site, ordre des opérations — est dans
[`2026-11-19-mise-en-coherence-grille.md`](../01_Administratif_et_Juridique/7_Documents_Legaux_SaaS/2026-11-19-mise-en-coherence-grille.md).
