# Mise en cohérence de la grille — état et plan d'action

> Rédigé le **2026-11-19** par Hotumana, après décision du fondateur :
> **Pro inchangé à 3 000 invités/mois**, **Business ramené à 10 000 invités/mois**.
> Objet : un seul jeu de valeurs, du contrat jusqu'à la jauge du dashboard.

## 1. La grille cible

| Plan | Lieux | Invités/mois |
|---|---|---|
| Free | 1 | 50 |
| Starter | 1 *(à confirmer)* | 1 000 |
| Pro | 3 *(à confirmer)* | **3 000** |
| Business | 10 *(à confirmer)* | **10 000** |
| Enterprise | Illimité | Illimité — sur devis |

**Seul le quota d'invités est arbitré.** Les valeurs « lieux » restent à trancher : elles diffèrent
partout (voir §2). Le fondateur n'a pas statué, je ne les change pas d'office.

## 2. L'état réel, support par support

| Support | Lieux Business | Invités Business | Statut |
|---|---|---|---|
| **CGV v1.3** (contrat) | 20 | **100 000** | à réécrire |
| **Annexe 5 SLA v1.1** | — | **100 000** | à réécrire |
| **Back-end / dashboard** | **20** | **100 000** | à modifier |
| **Grille Dodo / site** | 10 | 30 000 | à modifier |
| **Fiche produit (interne)** | 10 | 10 000 | ✅ alignée le 19/11 |

**Le point contre-intuitif :** le back-end et le contrat sont **d'accord** — à 100 000 invités et
20 lieux. C'est la vitrine commerciale (Dodo, site) et la fiche produit qui étaient en retard. La
baisse à 10 000 n'est donc pas une correction de texte : c'est un **changement de contrat** et un
**changement de code**.

## 3. Les documents légaux à réécrire

### 3.1 CGU/CGV v1.3 → v1.4

| Emplacement | Avant | Après |
|---|---|---|
| En-tête de version | « Version 1.3 — En vigueur au 11 octobre 2026 » | **Version 1.4 — En vigueur au [date de publication]** |
| Tableau § 4.1 — Pro | 10 lieux / 20 000 | **3 lieux / 3 000** |
| Tableau § 4.1 — Business | 20 lieux / 100 000 | **10 lieux / 10 000** |
| Tableau § 4.1 — Starter | 3 lieux / 1 000 | **1 lieu / 1 000** *(à confirmer)* |
| Article 12 | préavis de 30 jours | inchangé |
| Article 4.3 | révision des prix, 60 jours | inchangé |

⚠️ **Ne pas oublier le § 4.1 « Critères objectifs de classement »** (salariés / chiffre d'affaires) :
il rend le plan inapplicable à un établissement public. Le PAP ne peut pas être classé ainsi. Si
Enterprise reste « illimité », il faut lui donner une porte d'entrée qui ne passe pas par le CA.

### 3.2 Annexe 5 — SLA v1.1 → v1.2

| Emplacement | Avant | Après |
|---|---|---|
| § 8.2 — Capacité | « 100 000 invités/mois sur le plan Business » | **10 000 invités/mois sur le plan Business** |
| § 8.2 — Capacité | « Invités illimités sur le plan Enterprise » | inchangé |

C'est un **engagement de capacité** : le modifier à la baisse change ce que tu garantis. À faire
maintenant, tant qu'aucun client n'a signé — après, il faudrait un avenant.

### 3.3 Autres documents à balayer

- `7-Politique de remboursement v1.1` — vérifier si elle cite des plans ou des quotas.
- Annexes 1 (DPA), 3 (mentions légales) — a priori sans quotas, mais un contrôle ne coûte rien.
- Versions HTML publiées dans `C_Versions_HTML_Site_Web/` — ce sont elles que le client lit.

## 4. Le back-end

Le dashboard affiche des jauges « Lieux x/y » et « Invités x/y », avec alerte à 80 % et blocage au
plafond. Quatre points à vérifier :

| # | À vérifier | Pourquoi |
|---|---|---|
| 1 | La table / fonction qui porte les limites par plan | c'est la source unique — si elle n'existe pas, les limites sont codées en dur à plusieurs endroits |
| 2 | Les jauges du dashboard (x/20, x/100 000) | elles doivent lire la nouvelle source, pas une constante |
| 3 | L'alerte à 80 % | elle doit se déclencher sur 8 000, pas sur 80 000 |
| 4 | Le comportement au plafond | blocage, dépassement facturé, ou achat du pack +10 000 ? **À trancher** |

**Prompt à donner à Lovable :**

> « La grille des plans change : Business passe à 10 000 invités/mois, Pro à 3 000, Starter à 1 000.
> Mets à jour la source unique des limites par plan, les jauges du dashboard, les seuils d'alerte à
> 80 % et les textes de la page tarifs. Vérifie qu'aucune limite n'est codée en dur ailleurs. »

## 5. L'ordre des opérations

1. **Trancher les « lieux »** (1 / 3 / 10 ?) — sinon la moitié du travail sera à refaire.
2. **Back-end** : une seule source de vérité pour les limites.
3. **Documents légaux** : CGV v1.4 + annexe SLA v1.2, relus par l'avocat.
4. **Site et Dodo** : descriptions des plans alignées.
5. **Contrôle final** : créer un compte de test, vérifier jauge, alerte 80 %, blocage.

Ne jamais publier l'étape 4 avant l'étape 3 : une page tarifs qui annonce 10 000 alors que la CGV
dit 100 000, c'est exactement l'écart qu'on cherche à supprimer.

## 6. Point de vigilance commercial

La nouvelle échelle est **géométrique et cohérente** : 1 000 → 3 000 → 10 000, soit ×3 à chaque
étage. C'est plus lisible que l'ancienne (1 000 → 5 000 → 30 000, ×5 puis ×6).

Mais elle rend le **Business moins généreux** qu'annoncé partout. Deux conséquences :

- Les prix doivent suivre la même progression. Si Business était à 30 000 invités et reste au même
  tarif avec 10 000, c'est une hausse de prix de fait. **À vérifier dans Dodo.**
- Pour les trois premiers clients de référence, figer le quota par écrit (24 mois) évite qu'ils
  subissent la baisse en cours de route.
