-- FenuaFact — migration « relances automatiques »
-- À exécuter dans Supabase → SQL Editor. Idempotent.
-- Date : 2026-11-17

alter table public.devis add column if not exists nb_relances int not null default 0;
alter table public.devis add column if not exists derniere_relance timestamptz;
alter table public.devis add column if not exists date_envoi timestamptz;

-- Index pour le balayage quotidien
create index if not exists devis_relance_idx
  on public.devis (statut, nb_relances)
  where type_document = 'devis';
