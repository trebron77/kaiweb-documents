# État du projet WaveFi — point d'entrée

> **Dernière mise à jour : 22 novembre 2026.**
> À lire en premier. Si une information contredit ce fichier, ce fichier est probablement en retard :
> mets-le à jour avant de continuer.

---

## 1. Situation

- **Aucun client en production.** Aucun abonné, aucune facture émise, aucune donnée client sur le VPS.
- Projets Lovable : **Pixel Perfect Clone** (vitrine `wavefi.tech`), **WaveFi Marketing Cloud** (app
  `app.wavefi.tech`), **Fenua Voice Quotes** (projet distinct — ne pas confondre).
- Société : SASU KaiWeb Marketing en cours d'immatriculation. Siège 38 rue du Maréchal Foch, Papeete.
  Franchise en base de TVA.

## 2. Ce qui est fait

| Domaine | État |
|---|---|
| **Infrastructure** | VPS `31.220.21.53` monté à **8 Go / 96 Go / 2 vCPU** le 21/11. Portail et RADIUS vérifiés. |
| **Supervision** | `check_vps.py` toutes les 6 h, silencieux sauf incident. |
| **Grille tarifaire** | 9 990 / 26 900 / 79 900 · Enterprise dès 149 000 · lieux 1/3/10 · invités 1 000/3 000/10 000. |
| **Vitrine** | Tarifs publiés et vérifiés (CGU, SLA, pack, mention XPF). |
| **Application** | Grille en source unique, textes alignés, jauges et journal de support — **non publiée**. |
| **Documents légaux** | CGU-CGV **v1.4** (effet 22/11/2026), remboursement **v1.2**, Annexe 5 SLA **v1.2**. |
| **Dodo** | 7 produits (3 mensuels, 2 annuels, pack), libellé `DODO_PAY_WAVEFI`, 3D Secure activé. |
| **WhatsApp** | Numéro **+689 89 63 73 06** déjà sur l'API Cloud — test envoyé depuis l'app le 23/10/2026. |

## 3. Ce qui reste ouvert

| Sujet | Où c'est bloqué |
|---|---|
| **Business 12 mois** (Dodo) | produit en brouillon, plafond de panier 3 000 USD → demande à 10 000 USD **en cours d'examen** |
| **Vérification d'entreprise Meta** | en cours |
| **Modèles WhatsApp** | à déposer : `bienvenue_wifi`, `offre_du_mois`, `demande_avis` |
| **Envoi de campagnes** | à construire — c'est la valeur du produit, et elle n'existe pas encore |
| **Compteurs** | jauges en place, base d'événements à câbler sur l'envoi réel |
| **Le port** (8 Grands Comptes) | devis envoyé, attend la copie de la transmission au service informatique |
| **UniFi** | contrôleur à installer sur le VPS (la RAM le permet depuis le 21/11) |
| **CGU v1.4 sur le site** | la vitrine publie encore la v1.3 avec des prix neufs |

## 4. Les pièges à ne pas répéter

| Piège | La vérité |
|---|---|
| Numéros WhatsApp | **WaveFi = 89 63 73 06** · **FenuaFact = 87…**. Ne jamais mélanger. |
| Le numéro WaveFi serait « à migrer » | **Faux.** Il est déjà sur l'API Cloud depuis octobre. |
| Devise | Le code est **XPF**. « XFP » n'existe pas. |
| Facture Dodo | Toujours en **USD** même si le paiement est en XPF — d'où la note de conversion. |
| Taxe pour un client polynésien | **0 %**. Les 10 % d'un aperçu ne concernent pas nos clients. |
| Identifiant du pack | `pdt_0NsX5JzIGjhO3pETsGFX0` — finit par le **chiffre zéro**. |
| Renommer un produit Dodo | Sans risque sur les prix ; **jamais** sur ce que le produit donne (créer un nouveau). |
| « Enregistré » chez Lovable | ≠ « publié ». Vérifier sur `wavefi.tech`, jamais dans l'aperçu. |

## 5. Où trouver quoi

| Besoin | Fichier |
|---|---|
| Grille et application | `02_Produit_WaveFi/2026-11-22-application-grille-tarifaire.md` |
| Documents légaux | `01_Administratif_et_Juridique/7_Documents_Legaux_SaaS/` |
| Meta / WhatsApp | `ops/meta-whatsapp-etat.md` |
| Serveur | `ops/MAINTENANCE_VPS.md` |
| Grands comptes | `03_Commercial_et_Prospection/8_Grands_Comptes/` |
| Journal | `06_Suivi_Projet_et_Journal/` |
| Tests de paiement Dodo | `04_Finance_et_Comptabilite/5_Tests_Paiement_Dodo/` |

---

**Règle de tenue :** toute décision prise dans une conversation doit atterrir ici ou dans un fichier
cité ci-dessus, le jour même. Une décision qui ne vit que dans un chat est une décision perdue.
