# SEO / GEO — rapport externe vérifié

> Rapport ChatGPT du 23/11/2026 contrôlé sur le site en ligne le même jour.
> Verdict : **méthodologie correcte, données périmées**. Quatre constats sur cinq sont faux
> aujourd'hui, parce qu'ils décrivent l'état d'avant le 22/11.

## Ce que le rapport affirmait, et la réalité

| Affirmation | Réalité vérifiée |
|---|---|
| Tarifs : 4 995 / 12 950 / 34 950 | **9 990 / 26 900 / 79 900 / 149 000**, identiques sur `/tarifs` et `/legal/cgu` |
| Business 15 000 invités (tarifs) vs 10 000 (CGU) | **10 000 partout** |
| `robots.txt` inaccessible | **200** — autorise Googlebot, Bingbot et **OAI-SearchBot** |
| `sitemap.xml` inaccessible | **200**, **27 URL**, toutes en 200 |
| JSON-LD non inspectable | **présent et à jour** : `Organization`, `SoftwareApplication` + offres à 9 990 XPF, `FAQPage`, `BlogPosting` |
| Blog : 4 articles | **11 articles publiés** |

## Le point technique qui compte, et qu'il n'a pas vu

Le site est **rendu côté serveur** : un article renvoie 11 971 caractères de texte dans le HTML
brut. Les moteurs IA qui n'exécutent pas le JavaScript — dont beaucoup — peuvent donc lire le
contenu. C'est un avantage rare, et il est déjà en place.

## Ce qui reste réellement à faire

| # | Action | Qui |
|---|---|---|
| 1 | **Google Search Console + Bing Webmaster Tools** : déclarer le site, soumettre le sitemap | Norbert — c'est la seule chose qui puisse *confirmer* l'indexation |
| 2 | **Compléter les données structurées** : `BreadcrumbList`, `contactPoint`, `Product`/`AggregateOffer` sur `/tarifs`, champs manquants des `BlogPosting` | Lovable |
| 3 | **Autorité** : adhésion CCISM, partenariats avec agences digitales et installateurs Wi-Fi, premières mentions externes | Norbert |

## Ce qu'on ne fait pas, et pourquoi

Le rapport recommande de publier un « guide de référence » pour le GEO. Sur le fond, l'idée est
bonne. Dans les faits : **11 articles, 27 pages, zéro client**. Le contenu n'est pas le goulot
d'étranglement — la prospection l'est. Un douzième article ne produira pas le premier client ;
une adhésion CCISM et deux partenariats produiront des liens entrants, et ce sont eux qui font
l'autorité.

Le guide pourra être écrit quand il y aura des clients à citer dedans.

## Données structurées — état après publication du 23/11

Vérifié sur le HTML servi par `wavefi.tech` (pas dans l'éditeur).

| Élément | État |
|---|---|
| `sameAs` Facebook / LinkedIn | **supprimés** du balisage *et* du pied de page — les deux URL pointaient vers une page inexistante et vers une société américaine homonyme |
| `Organization` + `ProfessionalService` + `SoftwareApplication` | présents sur toutes les pages |
| `FAQPage` | accueil et articles |
| `BreadcrumbList` | pages internes (`Accueil › Tarifs`) |
| `Product` + offres | `/tarifs` : Free 0 · Starter 9 990 · Pro 26 900 · Business 79 900 XPF |
| `AggregateOffer` Entreprise | `lowPrice` 149 000 XPF, InStock |
| `BlogPosting` | **les 11 articles** en portent un |
| Dates | `datePublished` 2026-11-07 · `dateModified` 2026-11-23 — **identiques aux dates affichées** sur chaque page |

**Reste optionnel :** les quatre offres standard n'ont pas de champ `availability`. Google le tolère,
mais l'ajouter (`InStock`) complète la fiche. À faire lors d'une prochaine passe, pas urgent.
