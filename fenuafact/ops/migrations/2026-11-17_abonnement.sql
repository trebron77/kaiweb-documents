-- FenuaFact — migration « abonnement »
-- À exécuter dans Supabase → SQL Editor. Idempotent.
-- Date : 2026-11-17

alter table public.tenants add column if not exists abonnement_statut text not null default 'aucun';
-- Valeurs possibles : aucun | essai | actif | en_retard | suspendu | annule | expire

alter table public.tenants add column if not exists abonnement_fin timestamptz;
alter table public.tenants add column if not exists dodo_customer_id text;
alter table public.tenants add column if not exists dodo_subscription_id text;

create index if not exists tenants_dodo_subscription_idx
  on public.tenants (dodo_subscription_id);
