# Mise à jour de la grille tarifaire — textes à publier

> Préparé le **2026-11-22**. Cible : site vitrine, application, Dodo Payments.
> Grille validée : 9 990 / 26 900 / 79 900, quotas 1 000 / 3 000 / 10 000, lieux 1 / 3 / 10.

## 1. Le piège de séquence

La grille contient deux promesses que **le produit ne sait pas encore mesurer** :

- « 300 messages WhatsApp inclus par mois »
- « 20 minutes de support incluses par mois »

Si on les publie maintenant, on recrée exactement l'écart qu'on a passé une journée à corriger
entre les CGV et le back-end : une page qui promet, un produit qui ne compte pas.

**Règle proposée :**

| À publier maintenant | À garder pour plus tard |
|---|---|
| Prix mensuels | Quota de messages WhatsApp |
| Nombre de lieux | Heures de support incluses |
| Nombre d'invités par mois | Dépassements facturés |
| Fonctions par plan | — |

Les quotas de messages et de support restent dans la **CGV v1.4** (brouillon, non publiée) : ils
existeront contractuellement, et n'apparaîtront sur le site que le jour où le compteur existera.

## 2. Site vitrine — page tarifs

### Starter — 9 990 FCFP/mois

> **Pour un commerce indépendant qui veut capter ses clients.**
> 1 lieu · 1 000 invités par mois
> Portail captif à votre image, collecte d'e-mails, boost d'avis Google, campagnes e-mail.

### Pro — 26 900 FCFP/mois

> **Pour un établissement en croissance ou un petit réseau.**
> 3 lieux · 3 000 invités par mois
> Campagnes avancées, statistiques détaillées, gestion des contenus par lieu.

### Business — 79 900 FCFP/mois

> **Pour les chaînes et les groupes multi-sites.**
> 10 lieux · 10 000 invités par mois
> Gestion centralisée, analytics avancés, support prioritaire.

### Enterprise — sur devis, à partir de 149 000 FCFP/mois

> **Pour les grandes infrastructures d'accueil : ports, aéroports, terminaux.**
> Lieux et invités illimités · intégration à votre infrastructure existante (overlay) · engagement
> de service contractuel · interlocuteur dédié.
> *Devis établi selon votre périmètre — nous consulter.*

**Mention de bas de page :** « Tarifs en francs pacifique (FCFP), par mois. TVA non applicable —
franchise en base. »

## 3. Application — écran des plans

Trois valeurs à changer dans la source de vérité des limites :

| Plan | Lieux | Invités/mois |
|---|---|---|
| Free | 1 | 50 |
| Starter | 1 | 1 000 |
| Pro | 3 | 3 000 |
| Business | 10 | 10 000 |
| Enterprise | illimité | illimité |

Les jauges du dashboard, les seuils d'alerte à 80 % et les textes de la page tarifs doivent lire
**cette même source** — pas des constantes dispersées.

## 4. Dodo Payments — produits

| Produit | Prix | Description courte |
|---|---|---|
| WaveFi Starter | 9 990 XPF/mois | 1 lieu · 1 000 invités/mois |
| WaveFi Pro | 26 900 XPF/mois | 3 lieux · 3 000 invités/mois |
| WaveFi Business | 79 900 XPF/mois | 10 lieux · 10 000 invités/mois |

- L'ancien **Pack +10 000 invités** n'est plus cohérent avec un plafond Business à 10 000 → **à
  retirer**, ou à transformer en « Pack +5 000 invités » *(décision à prendre)*.
- Enterprise **ne passe pas par Dodo** : devis et facturation directe.

## 5. Ordre des opérations

1. Décider du sort du pack d'invités supplémentaires.
2. Mettre à jour **la source unique** des limites dans l'application.
3. Publier les prix sur le **site**.
4. Mettre à jour **Dodo**.
5. Contrôler : créer un compte de test, vérifier jauge, seuil 80 %, et le prix affiché au paiement.

> Ne jamais publier l'étape 3 avant l'étape 2 : une page tarifs à jour et un back-end à l'ancienne,
> c'est le défaut qu'on vient de corriger ailleurs.
