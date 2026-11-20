-- FenuaFact — migration « plan d'abonnement »
-- À exécuter dans Supabase → SQL Editor. Idempotent.
-- Date : 2026-11-18

alter table public.tenants
  add column if not exists abonnement_plan text not null default 'essentiel';

-- Valeurs : essentiel | pro
alter table public.tenants
  drop constraint if exists tenants_abonnement_plan_check;

alter table public.tenants
  add constraint tenants_abonnement_plan_check
  check (abonnement_plan in ('essentiel', 'pro'));
