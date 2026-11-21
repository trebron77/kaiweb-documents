# Achat de matériel — borne Wi-Fi et injecteur PoE

> Achat du **21 novembre 2026** chez **Formatik Tahiti**. Note établie pour la comptabilité et le
> suivi du dossier société.

## 1. Ce qui a été acheté

| Facture | Objet | HT | TVA 16 % | TTC |
|---|---|---|---|---|
| **FAC_2026_00107** | Point d'accès Ubiquiti UniFi **U6-LR** | 29 741 | 4 759 | **34 500** |
| **FAC_2026_00106** | **Injecteur PoE** Ubiquiti **U-POE-at-EU** | 4 224 | 676 | **4 900** |
| | **Total** | 33 965 | **5 435** | **39 400** |

- **Payé le 21/11/2026 par carte bancaire** — montant dû : 0.
- Factures établies au nom de **KAIMUKO Norbert** (`contact@wavefi.tech`), pas au nom de la SASU.

## 2. Comparatif fournisseurs

| Fournisseur | Montant TTC | Écart |
|---|---|---|
| **Formatik** (retenu) | **39 400 XPF** | — |
| Cybertech | 44 390 XPF | + 4 990 XPF (+ 12,7 %) |

## 3. Nature comptable

**Dépense personnelle de l'associé, pas un acte de la société.**

Les deux factures sont à son nom. Elles ne relèvent donc pas de l'état des actes de l'article 15
(qui ne couvre que les engagements pris au nom de la société en formation), mais du **compte courant
d'associé** — la convention est déjà au dossier (`1_Statuts_SASU/Convention_Compte_Courant_Associe.docx`).

À faire : inscrire 39 400 XPF au crédit du compte courant, sur présentation des deux factures.

**TVA :** 5 435 XPF d'ores et déjà payés, **non récupérables** en franchise en base. Le coût réel de
l'achat est donc bien de 39 400 XPF, pas de 33 965.

## 4. Le matériel

| Élément | Rôle | Statut |
|---|---|---|
| **U6-LR** | point d'accès Wi-Fi 6 — sert aux tests et aux démonstrations | **livraison mardi 25/11** |
| **U-POE-at-EU** | injecteur PoE+ 802.3at, 48 V — alimente la borne par le câble réseau | remis le 21/11 |

L'injecteur est le bon modèle : le U6-LR exige du **802.3at (PoE+)**, pas du 802.3af. Un injecteur
af aurait été insuffisant.

⚠️ **Payé d'avance sur un matériel non encore remis.** Demander un **bon de livraison** daté à la
remise de la borne : c'est la pièce qui prouve la livraison si un litige survient.

## 5. Suite

À réception de la borne : appliquer le runbook d'intégration (`ops/runbook-integration-portail-captif.md`, § 4 pour UniFi) — contrôleur, SSID invité, portail externe, walled garden, recette en 10 points.
