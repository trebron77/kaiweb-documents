# WaveFi — fiche produit (synthèse)

> Synthèse établie le 14/11/2026 à partir des documents du dossier et du journal `Journal_IA/`.
> À faire relire et corriger par le fondateur : c'est une reconstruction, pas une source officielle.

## 1. Positionnement

WaveFi est une **couche logicielle de WiFi marketing** qui se branche sur les routeurs déjà installés
dans un établissement (Ubiquiti, TP-Link, Zyxel, Ruijie, Edgecore…) pour transformer la connexion
WiFi des clients en outil de captation et de fidélisation.

Marché initial : **Polynésie française** — restaurants, bars, cafés, hôtels, boutiques, cliniques,
salles de sport. Cibles grands comptes : aéroport de Tahiti-Faa'a (ADT), Air Tahiti Nui (ATN),
Port Autonome de Papeete.

## 2. Fonctions

- **Portail captif personnalisé** à la marque de l'établissement.
- **Collecte de contacts** : e-mail, téléphone, login social.
- **Campagnes** : e-mail (Brevo), WhatsApp, SMS.
- **Boost d'avis Google** : relance automatisée des clients satisfaits.
- **Analytics** : nombre de clients uniques, contacts collectés, démographie, sessions.
- **Assistant IA** intégré.
- **Multi-lieux** et gestion centralisée pour les réseaux.
- **Marque blanche / revente** : contrat de revente + 5 annexes, checklist de signature, charte de
  marque blanche.

## 3. Stack technique (d'après le journal de build)

| Brique | Rôle |
|---|---|
| Lovable | Construction du front-end et de la logique applicative |
| Supabase / Lovable Cloud | Base de données, authentification, règles RLS, quotas, journaux d'audit |
| Dodo Payments | Paiement et abonnements (webhooks) |
| Brevo | E-mailing, campagnes, import de contacts |
| Meta WhatsApp Cloud API | Messages WhatsApp |
| OpenAI | Assistant IA du produit |

## 4. Offre tarifaire

| Plan | Cible | Inclus |
|---|---|---|
| **WaveFi Free** | Découverte | 1 lieu, 50 invités/mois |
| **WaveFi Starter** | Commerces indépendants (restos, snacks, bars) | 1 lieu, 1 000 invités/mois, portail captif, collecte d'e-mails, boost d'avis Google |
| **WaveFi Pro** | Établissements en croissance, petits réseaux | 3 lieux, 3 000 invités/mois, campagnes avancées, statistiques détaillées |
| **WaveFi Business** | Chaînes d'hôtels, groupes multi-sites | 10 lieux, 10 000 invités/mois, gestion centralisée, analytics avancés, support prioritaire |
| **WaveFi Entreprise** | Grands comptes publics et infrastructures d'accueil (PAP/TCI, aéroports) | Overlay sur infrastructure existante (Cisco, Aruba, Ruckus…), volume élevé, SLA et support prioritaire. **Sur devis — non publié dans la grille aujourd'hui** (voir [`2026-11-19-chiffrage-plan-entreprise.md`](../03_Commercial_et_Prospection/7_Offre_et_Tarifs/2026-11-19-chiffrage-plan-entreprise.md)) |
| **Pack +1 000 invités** | Pics de fréquentation | 1 000 invités supplémentaires/mois — **7 990 XPF**, limité à 1 pack par mois |

Détail et calcul du coût d'un set-up : `03_Commercial_et_Prospection/7_Offre_et_Tarifs/`.

## 5. Documents contractuels disponibles

- CGU/CGV v1.3 + annexes (DPA, cookies, mentions légales, confidentialité, SLA), politique de
  remboursement v1.1.
- Contrat de revente SaaS v1.1 + annexes (facturation, comptes réservés, SLA, documentation
  technique, charte marque blanche).
- Versions HTML publiées : `01_…/7_Documents_Legaux_SaaS/C_Versions_HTML_Site_Web/`.

## 6. Situation juridique (au 14/11/2026)

Société **SASU KAIWEB MARKETING** en cours de constitution à Papeete : statuts rédigés, relecture
avocat en cours de devis, domiciliation Papeete Coworking (facture n° 11112026 du 11/11/2026),
ouverture bancaire en préparation, dépôt CDFE à venir. Points de vigilance identifiés : RC Pro
couvrant les prestations informatiques et le traitement de données ; conformité RGPD / loi locale
sur les portails captifs.
