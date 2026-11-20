# FenuaFact — Reprise du projet MVP

> **Document de passation** — 2026-11-17
> Source principale : export du chat DeepSeek (585 pages mises en page, 46 tours, 210 K tokens) déposé le 2026-11-17.
> Source secondaire : lecture directe du code en production (`/var/www/fenuafact-api/main.py`, 336 lignes) et de l'infrastructure du VPS.
> Convention : ✅ = vérifié sur le serveur, 📄 = affirmé dans le chat, ❓ = à confirmer.

---

## 1. En une phrase

**FenuaFact** est un SaaS de **devis et factures par dictée WhatsApp** destiné aux artisans et TPE de Polynésie française, avec gestion native du **franc CFP (XPF)**, de la **TVA polynésienne** et du **numéro TAHITI**.

---

## 2. Contexte stratégique

Le produit n'est pas isolé : il s'inscrit dans une stratégie d'écosystème.

| Ordre | Produit | Rôle |
| --- | --- | --- |
| 1 | Générateur de leads B2B (déjà construit, WaveFi/Hotumana) | Acquérir des artisans et PME à bas coût — le « cheval de Troie » |
| 2 | **SaaS C — FenuaFact** (ce projet) | Le cœur du métier de l'artisan : devis/factures. Forte synergie, besoin quotidien, upsell naturel |
| 3 | SaaS B — Copilote financier (OCR + agrégation bancaire) | Upsell à forte valeur, une fois la confiance installée |
| 4 | SaaS A — Builder de tunnels de vente | Nouveau marché, à traiter séparément |

**Décision actée** : commencer par le SaaS C (facturation artisans), le produit le plus synergique avec la base clients existante. 📄

**Marchés** : Polynésie française d'abord, puis **Nouvelle-Calédonie** et **Wallis-et-Futuna**. 📄 Le modèle de données doit donc prévoir un identifiant d'entreprise générique (`business_registration_type` + `business_registration_number`, pas un champ « SIRET » figé) : TAHITI en PF, RIDET en NC.

**Concurrent identifié** : **VOX** (Nouvelle-Calédonie, « un artisan dicte, VOX fait le devis »). 📄 La différenciation FenuaFact : ancrage polynésien (XPF, TVA, TAHITI, français, accompagnement local).

---

## 3. Périmètre du MVP (v0.1)

| Dans le MVP 📄 | Plus tard (v0.2+) 📄 |
| --- | --- |
| Création de devis par **vocal WhatsApp** | Devis par appel téléphonique direct |
| Création manuelle de devis/factures (web) | Catalogue réutilisable (partiellement fait, voir §5) |
| Génération PDF conforme PF | Signature électronique (eIDAS) |
| Envoi du devis par WhatsApp ou email (Brevo) | Relances automatiques J+3 / J+7 |
| Conversion devis → facture en 1 clic | Paiement en ligne intégré (lien Dodo) |
| Suivi de statut (brouillon / envoyé / accepté / refusé / payé) | Gestion d'équipe, planning chantier |
| Mono-utilisateur (1 artisan = 1 entreprise) | Multi-utilisateurs par entreprise, rôles |
| Fiche client simple (nom, contact, adresse) | Import/export comptable |

**Règle d'or du périmètre** 📄 : chaque fonctionnalité doit répondre à « l'artisan peut-il facturer plus vite qu'avec un carnet et Word ? ». Si non → v0.2.

---

## 4. Spécificités Polynésie française (à ne jamais perdre)

- **Devise XPF** : zéro décimale. Montants **entiers** en base (`INTEGER`), jamais de `float`. Affichage `125 000 F CFP` avec espace insécable.
- **TVA** : **quatre** taux réels, selon la DICP ([source officielle](https://www.service-public.pf/dicp/faq-items/quels-sont-les-principaux-taux-de-tva/)) — **16 %** (normal, produits), **13 %** (intermédiaire, prestations de services), **5 %** (réduit : alimentaire, transport de voyageurs, électricité, hôtellerie), **1 %** (archipels autres que la Société, en vigueur depuis le 01/07/2026). ⚠️ Le chat annonçait « 13 % normal, 5 % réduit, 1 % particulier » : **c'est faux**. Les **services BTP relèvent du 13 %**, faute d'exonération générale. Mention obligatoire : « TVA acquittée sur les débits » ou « TVA non applicable, art. X ».
- **Identifiants** : numéro **TAHITI** en PF, **RIDET** en NC.
- **Mentions légales PDF** : raison sociale, adresse, n° TAHITI, numéro séquentiel chronologique, dates d'émission et de prestation, détail des lignes (désignation, quantité, PU HT, TVA, TTC), conditions de paiement, coordonnées bancaires si virement.
- **Numérotation** : format `DEV-2026-0001` / `FAC-2026-0001`, séquentiel par tenant et par année, **sans trou**. 📄
- **Délai de paiement par défaut** : 30 jours, configurable. 📄

---

## 5. Architecture réellement déployée ✅

```
Artisan (WhatsApp)
   │ vocal .ogg
   ▼
Meta WhatsApp Cloud API
   │ webhook HTTPS
   ▼
Nginx (api.fenuafact.com, Certbot TLS)
   │ proxy_pass
   ▼
uvicorn/FastAPI — 127.0.0.1:8001  (service systemd « fenuafact »)
   ├── Groq Whisper large-v3-turbo   → transcription FR
   ├── Groq gpt-oss-120b             → extraction JSON du devis
   ├── Supabase (Postgres + RLS)     → tenants, catalogue, devis
   ├── fpdf2                         → PDF local
   ├── WhatsApp Cloud API            → envoi du PDF
   └── Brevo                         → envoi email au client
```

| Brique | Réalité vérifiée |
| --- | --- |
| VPS | `srv2147350` — OVH/Hostinger, IP `194.163.44.206` ✅ |
| Code API | `/var/www/fenuafact-api/main.py`, 336 lignes, Python 3.14 ✅ |
| Service | `fenuafact.service` (systemd), `Restart=always`, enabled ✅ |
| Exposition | `https://api.fenuafact.com/webhooks/whatsapp` → joignable (403 sans token) ✅ |
| Front web | Lovable — `fenua-voice-quotes.lovable.app`, 5 pages protégées par Supabase Auth 📄 |
| Domaine | `fenuafact.com` (Namecheap), API sur sous-domaine 📄 ✅ |
| Dépendances | fastapi 0.163.1, uvicorn 0.54.0, groq 1.7.0, fpdf2 2.9.0, supabase 2.34.1, httpx 0.28.1 ✅ |

**Endpoints existants** ✅ : `GET/POST /webhooks/whatsapp` (vérification Meta + réception), `POST /api/relance` (relance email Brevo).

**Modèle de données en production** (réel, plus simple que la cible) ✅ :
- `tenants` — nom_entreprise, numero_tahiti, email, taux_tva, franchise_tva
- `catalogue` — nom_article, prix_unitaire_xpf, tenant_id
- `devis` — client, articles (JSONB), notes, statut

> ⚠️ **Écart majeur** : le schéma cible conçu dans le chat prévoyait `documents` / `document_lines` / `document_events` (+ numérotation, TVA par ligne, conversion devis→facture, audit). Le code utilise une table `devis` simplifiée. Le MVP a été construit en raccourci, volontairement, pour valider le flux vocal.

---

## 6. Ce qui fonctionne (prouvé)

- ✅ **19 vocaux réels** et **5 devis PDF** générés dans le dossier de l'API — preuve d'usage réel, pas de test artificiel.
- ✅ **Test du 2026-11-16** : vocal « 4 heures de main-d'œuvre et un déplacement » → client « Marie », prix récupérés seuls dans `catalogue` (5 500 F/h, 1 500 F déplacement), calcul 23 500 F, nom « Artisan Test » et TAHITI repris de `tenants`, PDF envoyé sur WhatsApp.
- ✅ Vérification du webhook Meta : `hub.challenge` renvoyé en 200 avec le bon token, 403 sinon.
- ✅ Envoi email du devis via Brevo + endpoint de relance.
- ✅ Front Lovable : 5 pages protégées par authentification, formulaires fonctionnels en clair et en sombre, sauvegardes validées. 📄

**Le cœur du produit — « dicter un vocal, recevoir un devis PDF » — fonctionne de bout en bout.**

---

## 7. Dettes techniques et risques (priorisés)

| # | Problème | Impact | Sévérité |
| --- | --- | --- | --- |
| 1 | ~~**5 secrets en clair** dans `main.py`~~ | ✅ **Résolu le 2026-11-17** : migrés vers `.env` (chmod 600), chargés par `os.environ`, `.gitignore` en place. **Reste la rotation** des clés chez Meta/Groq/Supabase/Brevo | 🔴 → 🟡 |
| 2 | ~~`TENANT_ID` codé en dur (`1111…1111`)~~ | ✅ Résolu : tenant résolu par `tenants.telephone` (numéro WhatsApp de l'artisan), avec repli pilote. **Reste à renseigner le champ** | 🟡 |
| 3 | ~~`LAST_PDF` stocké en mémoire~~ | ✅ Persisté dans `media/last_pdf.json` | ✅ |
| 4 | ~~Aucune vérification de signature du webhook Meta~~ | ✅ Code HMAC-SHA256 en place ; **reste à renseigner `META_APP_SECRET`** | 🟡 |
| 5 | ~~`.ogg` et `.pdf` écrits dans le dossier de l'app~~ | ✅ Déplacés dans `media/` + purge cron à 30 jours | ✅ |
| 6 | ~~`except Exception` renvoie `str(e)` au client WhatsApp~~ | ✅ Message générique, trace côté serveur | ✅ |
| 7 | ~~CORS `allow_origins=["*"]`~~ | ✅ Restreint au front Lovable | ✅ |
| 8 | ~~Aucun healthcheck~~ | ✅ `GET /health` + surveillance 5 min avec alerte Discord | ✅ |
| 9 | Pas d'upload du PDF vers Supabase Storage (spec prévoyait un lien signé) | Dépendance au disque local | 🟡 |
| 11 | Abonnement et encaissement | ✅ Dodo Payments en **production** : produits live, clé, webhook, paiement réel validé puis remboursé. Changement d'offre opérationnel côté API | 🟡 bouton front à ajouter |
| 10 | ~~Facture, numérotation séquentielle, conversion devis→facture absents~~ | ✅ Livrés le 2026-11-17 : `FAC-2026-0001`, conversion en un appel, PDF conforme. **Reste : bouton « Convertir » dans le front** | 🟡 |

---

## 8. Incident du 2026-11-17 (résolu)

Le service était **arrêté depuis 00:44 UTC** : `SyntaxError` ligne 276 (`"notes": …` sans virgule, juste avant `"statut": "Envoyé"`). Uvicorn ne démarrait plus, systemd bouclait sur 5 redémarrages puis abandonnait. **Corrigé et redémarré le 2026-11-17 à 01:51 UTC**, webhook revalidé (200/403). Sauvegarde : `main.py.bak.20261117-015113`.

**Cause racine** : une modification a été appliquée sans vérification de syntaxe, et aucune supervision ne surveille le service (le `Restart=always` masque l'échec en boucle). C'est exactement le trou que la mise en place d'un healthcheck comblera.

---

## 9. Où le chat s'est arrêté

Dernier état 📄 : les **5 pages** du front sont protégées, le compte de test a validé sauvegardes et facturation puis a été supprimé — **reste à publier** (déploiement Vercel/Lovable). Supabase signale une **protection contre les mots de passe compromis désactivée**, à activer à part.

Puis : `Usage limit reached. Your limit will reset on Nov 17, 2026 at 07:00.` — c'est la fin du quota DeepSeek qui a interrompu le projet, pas une erreur technique.

---

## 10. Prochaines actions recommandées (dans cet ordre)

1. **Sécuriser les secrets** → `.env` + `python-dotenv`, rotation des 5 clés, `.gitignore`. (Le token WhatsApp et la clé Supabase `service_role` ont circulé dans un fichier non protégé.)
2. **Publier le front** Lovable (bloqué en fin de chat) et vérifier le parcours complet inscription → paramètres → catalogue.
3. **Multi-tenant minimal** : résoudre le tenant depuis le JWT Supabase au lieu de la constante, sinon le produit n'est pas vendable.
4. ✅ *Fait le 2026-11-17* — **Facture** : conversion devis → facture, numérotation `FAC-2026-0001` atomique et sans trou, PDF conforme avec dates d'émission et d'échéance.
5. **Durcissement API** : vérification de signature webhook, purge des fichiers, gestion d'erreurs propre, healthcheck `GET /health` supervisé.
6. **Dodo Payments** : transaction test en XPF (devise à zéro décimale) avant d'intégrer l'abonnement.
7. **Tests terrain** avec 2–3 artisans pilotes.

---

## 11. Questions ouvertes — réponses du 2026-11-17

| Question | Réponse | Suite |
| --- | --- | --- |
| Front Lovable synchronisé sur GitHub ? | ❓ Inconnu — à vérifier | Contrôler le dépôt Lovable ; exporter le code pour éviter le lock-in |
| Transaction test Dodo en XPF ? | ❌ Pas encore faite | À faire avant toute intégration d'abonnement |
| BTP exonéré de TVA en PF ? | ✅ **Non** — aucune exonération générale : les services relèvent du **13 %**. Quatre taux réels (16/13/5/1), cf. §4 | Le moteur de TVA doit proposer les quatre taux, jamais un taux figé |
| Numéro WhatsApp dédié ? | ✅ Oui, carte SIM dédiée — confirmé | Rien à faire |
| Les 5 pages du front ? | ✅ Paramètres entreprise, catalogue, liste des devis, détail, clients | Publier |

**Reste à trancher** (décision produit) : comment identifier l'artisan (tenant) quand plusieurs clients partagent le même numéro WhatsApp business — voir dette n°2.

---

## 12. Sources

- Export du chat : `product/sources/2026-11-17-chat-export-585p.txt` (792 Ko, 14 877 lignes, 46 tours)
- Code : `/var/www/fenuafact-api/main.py` (production, sauvegarde datée à côté)
- Infrastructure : systemd, Nginx, certificats, dépendances — vérifiés le 2026-11-17
