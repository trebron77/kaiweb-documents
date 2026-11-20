# Audit du front (dépôt GitHub) — 2026-11-18

Dépôt : `trebron77/fenua-voice-quotes` (privé)
Stack : TanStack Start + React 19 + Vite + Supabase + Tailwind v4 + shadcn/Radix
Tests : 8 fichiers de test (routes, documents, abonnement, admin…)

## Ce qui va bien

- **Aucun secret dans le code.** Le seul accès sensible est `SUPABASE_SERVICE_ROLE_KEY`,
  lu depuis l'environnement côté serveur (`src/integrations/supabase/client.server.ts`),
  jamais versionné.
- Le client navigateur utilise la clé **publishable** — normal et attendu.
- Les appels API sont centralisés dans `src/lib/*.functions.ts` (documents, devis, admin, relance).
- La page Abonnement gère correctement : récupération du JWT, confirmation, état de chargement,
  rafraîchissement de la requête après succès.

## Points à corriger

1. ~~`.env` est versionné et absent du `.gitignore`~~ — **clos le 2026-11-18 : contrainte de plateforme.**
   Les builds publiés par Lovable Cloud n'embarquent que les fichiers commités : sortir `.env` du dépôt
   casserait le site. Le fichier ne contient que des valeurs publiques (URL, project id, clé *publishable*).
   **Règle à appliquer :** aucun secret dans `.env` ; les secrets vivent dans le coffre Lovable, et jamais
   derrière un préfixe `VITE_` (compilé dans le bundle navigateur). `.env.example` documente les noms.

2. **`abonnement.tsx` appelle l'API en direct** (`fetch` dans le composant), alors que tous les
   autres appels passent par `src/lib/`. Incohérence, et l'URL est codée en dur.
   → Extraire dans `src/lib/abonnement.functions.ts`.

3. **Erreurs affichées de deux façons** : `toast` pour le changement d'offre, `alert()` pour le
   checkout. → Uniformiser sur `toast`.

4. **Accès superadmin** : `admin.functions.ts` utilise la clé `service_role` (contournement total
   des RLS), protégé par `has_role('super_admin')`. C'est acceptable, mais c'est la surface la plus
   sensible du front : toute évolution doit conserver ce garde-fou côté serveur.

## Points d'attention non bloquants

- 53 dépendances d'exécution (Radix/shadcn). Poids de bundle, pas de risque.
- Les tests utilisent des sessions simulées : le parcours réel reste à valider manuellement.

## Accès

Clé de déploiement en lecture seule ajoutée par le propriétaire (`fenua-audit`), à supprimer
quand l'audit n'est plus nécessaire.
