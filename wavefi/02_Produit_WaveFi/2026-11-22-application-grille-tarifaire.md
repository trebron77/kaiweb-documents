# Application de la grille tarifaire — site, application, Dodo

> Rédigé le **2026-11-22**. À garder ouvert pendant la saisie.
> Grille validée : 9 990 / 26 900 / 79 900 · quotas 1 000 / 3 000 / 10 000 · lieux 1 / 3 / 10.
> Remise d'engagement : **−10 % pour 12 mois réglés d'avance**. Le −15 % est réservé aux trois
> premiers clients, contre référence écrite — ce n'est pas une offre publique.

## L'ordre, et pourquoi il n'est pas négociable

| # | Où | Pourquoi à ce moment-là |
|---|---|---|
| 1 | **Dodo** | personne ne peut acheter tant que les produits n'existent pas |
| 2 | **Application** | la source unique des limites doit être juste avant d'être affichée |
| 3 | **Site** | c'est la vitrine : elle ne doit pas promettre plus que le produit |
| 4 | **Tests** | un compte de test vaut mieux qu'une relecture |

---

## 1. Dodo Payments — les produits à créer

### Mensuels

| Nom du produit | Prix | Description |
|---|---|---|
| **WaveFi Starter — mensuel** | **9 990 FCFP**/mois | 1 lieu · 1 000 invités/mois |
| **WaveFi Pro — mensuel** | **26 900 FCFP**/mois | 3 lieux · 3 000 invités/mois |
| **WaveFi Business — mensuel** | **79 900 FCFP**/mois | 10 lieux · 10 000 invités/mois |

### Annuels, remise 10 % incluse

| Nom du produit | Prix | Correspond à |
|---|---|---|
| **WaveFi Starter — 12 mois** | **107 892 FCFP**/an | 9 990 × 12 − 10 % |
| **WaveFi Pro — 12 mois** | **290 520 FCFP**/an | 26 900 × 12 − 10 % |
| **WaveFi Business — 12 mois** | **862 920 FCFP**/an | 79 900 × 12 − 10 % |

### Option

| Nom du produit | Prix | Règle |
|---|---|---|
| **Pack +1 000 invités — mensuel** | **7 990 FCFP**/mois | 1 seul pack par mois et par contrat |

**À vérifier avant de créer :** que Dodo accepte le **XPF** (les anciens plans y étaient, mais la
devise doit être confirmée), et que la remise est **dans le prix du produit**, pas dans un code promo
— un code se perd et ne dit pas « engagement 12 mois ».

**Ne pas créer :** de produit Enterprise. Il passe par devis.

---

## 2. Application — la source unique des limites

Trois valeurs à changer, une seule fois, là où le produit les lit :

| Plan | Lieux | Invités/mois |
|---|---|---|
| Free | 1 | 50 |
| Starter | 1 | 1 000 |
| Pro | 3 | 3 000 |
| Business | 10 | 10 000 |
| Enterprise | illimité | illimité |


### Correspondance produits Dodo → plans de l'application

> Identifiants **copiés depuis le tableau de bord Dodo** les 22 et 24/11/2026 (bouton de copie).
> Préfixe `pdt_` en minuscules — la casse compte.

| Produit Dodo | Identifiant | Plan applicatif |
|---|---|---|
| WaveFi Starter | `pdt_0Nr6slWtU9ADTw47cvZhN` | Starter |
| WaveFi Pro | `pdt_0Nr6t27lv63qk6WvSBddY` | Pro |
| WaveFi Business | `pdt_0Nr6tGhdGGNYuaqx0lZO5` | Business |
| Starter 12 mois | `pdt_0NsX2RTJhtoNegWB40Liq` | Starter |
| Pro 12 mois | `pdt_0NsX2psrlXtirqXBNi2CC` | Pro |
| Business 12 mois | `pdt_0NseKgpbrsyb0vQr8XKyn` | Business |
| Pack +1 000 invités | `pdt_0NsX5JzIGjhO3pETsGFX0` | option, pas un plan |
| Pack +10 000 invités *(archivé)* | `pdt_0Nr6tVcOw8pIBOcw9o84W` | conservé pour les abonnés existants |

**Comment l'application identifie le plan :** par identifiant produit, jamais par le nom ni par le
prix. Si l'identifiant est inconnu, elle se rabat sur l'étiquette « plan » transmise avec le paiement.

**Point de vigilance :** le pack ne change jamais le plan — il ajoute seulement des invités.

Puis vérifier que **les jauges du dashboard, le seuil d'alerte à 80 % et les textes de la page
tarifs** lisent cette même source. Si une limite est écrite en dur ailleurs, elle y restera quand tu
changeras la grille dans deux ans.

---

## 3. Site — les textes finaux

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
> Lieux et invités illimités · intégration à votre infrastructure existante · engagement de service
> contractuel · interlocuteur dédié.
> *Devis établi selon votre périmètre — nous consulter.*

### Bandeau d'engagement, sous le tableau

> **−10 %** pour 12 mois réglés d'avance. Offre de lancement, hors intégration.

### Mention de bas de page

> Tarifs en francs pacifique (FCFP), par mois. **TVA non applicable — franchise en base.**

---

## 4. Ce qu'on ne publie pas encore

| Élément | Pourquoi | Où il vit en attendant |
|---|---|---|
| « 100 messages WhatsApp inclus » | le produit ne compte pas les messages | CGV v1.4, article tarifaire |
| « 20 min / 1 h / 2 h de support incluses » | idem pour le temps | CGV v1.4 |
| Les tarifs de dépassement (15 XPF/message, 7 500 XPF/h) | supposent un compteur | CGV v1.4 |

Le jour où le compteur existe, ces trois lignes remontent sur le site — et nulle part avant.

---

## 5. Tests, avant de considérer que c'est fait

| # | Test | Attendu |
|---|---|---|
| 1 | Créer un compte de test sur le plan Starter | jauge « 0 / 1 000 invités », « 1 lieu » |
| 2 | Passer au plan Pro | jauge mise à jour sans rechargement de configuration |
| 3 | Dépasser 80 % du quota sur un compte de test | alerte affichée |
| 4 | Aller au paiement Starter mensuel | **9 990 FCFP**, pas 4 995 |
| 5 | Aller au paiement Starter annuel | **107 892 FCFP** |
| 6 | Vérifier la mention TVA sur la page de paiement | « TVA non applicable — franchise en base » |
| 7 | Relire la page tarifs sur un téléphone | trois offres lisibles sans zoom |

---

## Checklist — tout changement de grille tarifaire

Un prix apparaît à **six endroits**. Aucun ne se met à jour tout seul.

| # | Endroit | Qui le porte |
|---|---|---|
| 1 | **Grille en base de données** | la source de référence |
| 2 | **Textes de l'application** — `tarifs.ts`, `register.tsx`, `aide.tsx`, `assistant-prompt.ts` | à aligner, puis lancer les tests |
| 3 | **Produits Dodo** — prix et descriptions | le tableau de bord |
| 4 | **Vitrine** (`wavefi.tech`, projet « Pixel Perfect Clone ») | projet Lovable séparé, aucune donnée partagée |
| 5 | **CGV** — article 4.1, grille tarifaire | document juridique |
| 6 | **Ce document** | la trace écrite |

**La règle :** un changement de prix n'est terminé que quand les six lignes sont cochées. L'application et la vitrine n'échangent aucune donnée — c'est un travail manuel, donc oubliable.

**Le test qui protège :** l'app compare sa grille à ses propres textes. Il ne peut rien voir de la vitrine ni de Dodo. C'est pourquoi les points 4 et 5 restent à la charge de l'opérateur.
