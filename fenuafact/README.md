# FenuaFact

## Contexte

SaaS de **devis et factures par dictée WhatsApp** pour les artisans et TPE de **Polynésie française**, avec extension prévue en **Nouvelle-Calédonie** et à **Wallis-et-Futuna**. L'artisan envoie un vocal WhatsApp ; le bot transcrit, comprend, chiffre, génère un PDF conforme et le lui renvoie.

FenuaFact est le **SaaS C** de l'écosystème décrit dans la stratégie « cheval de Troie » : le générateur de leads B2B existant sert de canal d'acquisition, FenuaFact apporte l'outil indispensable du quotidien, puis les produits finance et tunnels viennent en upsell.

## Objectif

Permettre à un artisan de facturer **plus vite qu'avec un carnet et Word**, sans changer ses habitudes : il dicte, il envoie. Objectif commercial : premier revenu récurrent sur la base clients existante, puis validation du modèle de cross-sell.

## Périmètre

**Inclus (v0.1)** : devis par vocal WhatsApp, devis/factures manuels côté web, PDF conforme PF (XPF, TVA 13/5/1 %, n° TAHITI), envoi WhatsApp ou email, statuts, fiche client simple, mono-utilisateur.

**Exclu (v0.2+)** : appel téléphonique direct, signature électronique, relances automatiques, paiement en ligne dans la facture, multi-utilisateurs et rôles, import comptable, planning chantier.

## Arborescence

| Dossier | Rôle |
| --- | --- |
| `product/` | Spécifications, reprise du projet, backlog, écarts code/spec |
| `ops/` | Infrastructure VPS, service, supervision, runbooks, incidents |
| `legal/` | Mentions légales PF, TVA, données personnelles, contrats |
| `growth/` | À créer — acquisition des artisans, tunnel, mesure |

## Règles propres au projet

1. **XPF = entiers.** Jamais de `float` pour un montant. Formatage `125 000 F CFP`.
2. **Conformité PF d'abord.** TVA à trois taux + exonération, numéro TAHITI, mentions légales obligatoires sur chaque PDF.
3. **Un numéro séquentiel sans trou.** La numérotation `DEV-2026-0001` / `FAC-2026-0001` est une obligation, pas un détail.
4. **Aucun secret dans le code.** Les cinq clés actuelles doivent migrer en `.env` (voir `ops/ETAT_TECHNIQUE.md`).
5. **Ne jamais modifier `main.py` sans vérifier la syntaxe.** La panne du 2026-11-17 venait d'une virgule manquante.

## Accès et environnement

| Élément | Valeur |
| --- | --- |
| VPS | `srv2147350` — `194.163.44.206` |
| API (prod) | `/var/www/fenuafact-api` — `https://api.fenuafact.com` |
| Service | `systemctl status fenuafact` (uvicorn, port 8001 en local) |
| Front (production) | **https://fenuafact.com** — publié par Lovable |
| Front (aperçu) | `fenua-voice-quotes.lovable.app` |
| Données | Supabase (projet managé) — `tenants`, `catalogue`, `devis` |
| Domaine | `fenuafact.com` (Namecheap) |

*Aucun secret dans ce dossier : les clés vivent dans l'environnement du VPS ou un gestionnaire dédié.*

## État actuel

**Le produit est en production sur https://fenuafact.com.** Les abonnements sont facturés en réel via Dodo Payments (offres Essentiel 7 950 XPF et Pro 12 900 XPF, changement d'offre géré, relances réservées au Pro). Le parcours complet fonctionne : vocal WhatsApp → devis numéroté et PDF → email au client → conversion en facture. Les cinq clés ont été remplacées et les anciennes révoquées le 2026-11-17. Restent avant la vente : le passage de l'application Meta en mode Live, le numéro TAHITI et l'abonnement Dodo.

Détail complet et dettes restantes : [`product/REPRISE_MVP.md`](product/REPRISE_MVP.md).

## Priorité actuelle

1. ✅ *Fait* — Secrets sortis de `main.py` vers `.env` (2026-11-17). Reste la **rotation** des 5 clés.
2. Publier le front Lovable.
3. ✅ *Fait* — Tenant résolu par le numéro WhatsApp de l'artisan. Reste à renseigner `tenants.telephone` et à exposer le champ dans les paramètres du front.

## Historique

| Date | Événement |
| --- | --- |
| 2026-11 (session DeepSeek) | Stratégie, choix du SaaS C, spécifications, schéma SQL, setup Meta, VPS, Supabase, pipeline vocal complet, front Lovable. Fin sur quota atteint. |
| 2026-11-16 | Premiers devis réels générés par vocal (19 vocaux, 5 PDF). |
| 2026-11-17 | Reprise du projet : import du chat (585 p.), diagnostic, **correction du service arrêté** (SyntaxError), rédaction de la passation. |
| 2026-11-17 | Mise en production : secrets migrés en `.env` puis **rotation complète des 5 clés** (Supabase, Meta, Groq, Brevo, verify token), multi-tenant par numéro WhatsApp, facture numérotée, PDF Unicode, supervision à trois états, front publié sur **https://fenuafact.com**. |
