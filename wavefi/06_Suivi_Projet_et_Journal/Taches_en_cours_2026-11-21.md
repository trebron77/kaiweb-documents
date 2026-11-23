# Tâches en cours — 2026-11-21

> **Note de transfert.** Reprend celle du 20/11 (dossier société). Concerne la société **KaiWeb
> Marketing** et le projet **WaveFi**.
> À lire au début de toute session reprenant le dossier.

## Fait le 21 novembre 2026

| # | Action | Où c'est consigné |
|---|---|---|
| 1 | **Renvoi d'appel `87 04 51 05 → 87 07 70 19` opérationnel** — testé avec un technicien Vini | — |
| 2 | **Achat matériel Formatik** : borne U6-LR (34 500 TTC) + injecteur U-POE-at-EU (4 900 TTC) = **39 400 TTC**, payé par carte | `04_Finance_et_Comptabilite/2026-11-21-achat-materiel-formatik.md` |
| 3 | **Comparatif fournisseurs** : Formatik 39 400 contre Cybertech 44 390 → Formatik retenu (− 4 990) | même note |
| 4 | Statuts : ligne « honoraires relatifs à la relecture par un avocat » **retirée** de l'annexe 3 | `1_Statuts_SASU/Satut SASU.docx` |
| 5 | Annexe article 15 (état des actes) : **déjà intégrée** au docx, sections 1 à 4 | `1_Statuts_SASU/Satut SASU.docx` |
| 6 | **Runbook d'intégration du portail captif** rédigé et publié (fiche Alcatel-Lucent, recette, lexique) | `ops/runbook-integration-portail-captif.pdf` |

## En attente active

| # | Sujet | Échéance | Bloqué par |
|---|---|---|---|
| 1 | **Borne U6-LR** — livraison, puis **demander un bon de livraison daté** (payée d'avance) | **mardi 24/11** | fournisseur |
| 2 | **PAP** — copie du commandant attendue ; **SMS de relance** s'il n'y a rien | **mardi 24/11** | le commandant |
| 3 | **Contrôleur UniFi sur le VPS** — à installer avant l'arrivée de la borne | avant le 24/11 | rien |
| 4 | **MyWiFi** — résiliation : aucun lieu à exporter ; puis corriger la CGV v1.4 et l'annexe 4 | — | décision prise |
| 5 | **CGV v1.4 + annexe SLA v1.2** — brouillons prêts (quotas, classement, franchise en base) | — | validation |
| 6 | **Devis PAP DEV-2026-001** — prêt (2 268 000 XPF année 1), **inexpediable avant le TAHITI** | — | immatriculation |

## À faire — lundi 23 novembre (inchangé)

| Heure | Qui | Question |
|---|---|---|
| 7h45 | Banque | Compte de dépôt pour SASU, 100 000 FCFP sur 200 000 ? |
| 8h30 | DAF — 40 47 18 18 | Droit d'enregistrement des statuts, rendez-vous nécessaire ? |
| 9h00 | CCISM — 40 47 27 00 | Formulaire M1 en ligne ? Rendez-vous ? |

Puis : ouverture du compte → versement 100 000 → signature des statuts →
enregistrement DAF (sous 1 mois) → annonce légale → dépôt CCISM → TAHITI.

## Points ouverts, hors société

| # | Action | État |
|---|---|---|
| 1 | Appeler le commandant de port | ✅ fait le 19/11 — relance mardi 24/11 |
| 2 | Contacter la cousine chez Tahiti Tourisme | à faire |
| 3 | Renvoi d'appel `87 04 51 05 → 87 07 70 19` | ✅ **fait** le 21/11 |
| 4 | Bascule des numéros publics (PDF, mentions légales, contact) | possible depuis le 21/11 — ⚠️ ne pas toucher au numéro du compte WhatsApp Business avant migration Meta |
| 5 | Vérification Meta Business | après immatriculation |
| 6 | Dépôt des marques FenuaFact et WaveFi | après TAHITI |
| 7 | Assurance RC pro | `6_Assurances/` — avant les premiers clients payants |
| 8 | PWA (FenuaFact) | après la bascule des numéros |

## Comment reprendre dans une autre session

> « Lis `wavefi/06_Suivi_Projet_et_Journal/Taches_en_cours_2026-11-21.md`, puis reprends le dossier
> société. »

## État commercial — à retenir

**Aucun client en production au 22/11/2026.** Aucun abonné, aucune facture émise, aucune donnée
client sur le VPS.

Conséquences pratiques, à ne pas oublier avant de proposer une migration ou une transition :
- les changements de version de CGV ne concernent personne — pas d'avenant, pas de préavis ;
- une remise en état de la base ou des produits Dodo ne casse aucun abonné ;
- les 130,18 zł d'écart constatés sur la facture Hostinger H55430228 n'ont aucun impact comptable
  puisqu'aucune vente n'a eu lieu.

Le jour où le premier client signe, cette section devra être mise à jour — elle conditionne la
plupart des précautions que nous prenons aujourd'hui.

### Dodo Payments — état vérifié le 22/11/2026

- **Vérification (KYC) validée** : l'encaissement en mode **live** fonctionne. Ne pas confondre avec un
  compte « particulier » — la mention `DODO_PAY_INDIVIDUAL` sur le reçu est le **libellé bancaire
  par défaut** (statement descriptor), personnalisable depuis les réglages Dodo. À remplacer par la
  dénomination de l'entreprise.
- Taxe appliquée à un client polynésien : **0 %** (vérifié sur facture réelle, 23/10/2026).
- Devise : les totaux du reçu client sont en **CFP**, la ligne produit apparaît en USD (affichage
  interne Dodo).
- Plafond de panier : **3 000 USD**, demande de relèvement à 10 000 USD déposée le 22/11.
