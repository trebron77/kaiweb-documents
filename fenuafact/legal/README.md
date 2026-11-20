# FenuaFact — conformité et mentions légales

> Ce dossier contient les règles de conformité, pas les documents signés. Les pièces officielles (statuts, attestations) restent chez le porteur de projet.

## 1. Fiscalité polynésienne

| Élément | Règle |
| --- | --- |
| Devise | Franc CFP (XPF) — **zéro décimale**, montants entiers |
| TVA | **16 %** normal (produits) · **13 %** intermédiaire (prestations de services, donc BTP) · **5 %** réduit (alimentaire, transport de voyageurs, électricité, hôtellerie) · **1 %** archipels hors Société (depuis le 01/07/2026) |
| Franchise en base | Mention « TVA non applicable, franchise en base » |
| Mention alternative | « TVA acquittée sur les débits » selon le régime |
| Identifiant | **Numéro TAHITI** de l'entreprise émettrice |

*Le BTP ne bénéficie d'aucune exonération générale : les prestations d'artisan relèvent du taux intermédiaire de 13 %. Seule la franchise en base (petits chiffres d'affaires) permet la mention « TVA non applicable ». Seuil et régime exact à confirmer avec le comptable, ainsi que le taux applicable aux travaux réalisés hors îles de la Société (1 %).*

## 2. Mentions obligatoires sur devis et factures

- Raison sociale, adresse, numéro TAHITI
- Numéro séquentiel et chronologique, **sans trou**
- Date d'émission et date de prestation
- Détail des lignes : désignation, quantité, prix unitaire HT, TVA, total TTC
- Conditions de paiement (délai, pénalités de retard)
- Coordonnées bancaires si virement

## 3. Numérotation

`DEV-2026-0001` / `FAC-2026-0001` — séquentiel **par tenant et par année**. Un numéro sauté est une non-conformité : la génération doit être transactionnelle.

## 4. Données personnelles

- Les données clients (nom, email, téléphone, adresse) sont hébergées chez **Supabase** (managé).
- La réglementation polynésienne sur la protection des données est distincte du RGPD : cadre à confirmer avant commercialisation.
- Le front doit rester **inaccessible sans authentification** (vérifié : 5 pages protégées).
- Point ouvert signalé par Supabase : activer la **protection contre les mots de passe compromis**.

## 5. Ce qui n'est pas encore couvert

- Conditions générales de vente / d'utilisation
- Contrat de sous-traitance avec les artisans utilisateurs
- Politique de conservation et de suppression des données
- Registre des traitements
