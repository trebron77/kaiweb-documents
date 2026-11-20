-- FenuaFact — migration « facture et numérotation »
-- À exécuter dans Supabase → SQL Editor. Idempotent : peut être rejoué sans risque.
-- Date : 2026-11-17

-- 1. Colonnes de document sur la table devis (elle porte devis ET factures)
alter table public.devis add column if not exists numero text;
alter table public.devis add column if not exists type_document text not null default 'devis';
alter table public.devis add column if not exists parent_id uuid references public.devis(id);
alter table public.devis add column if not exists date_emission date not null default current_date;
alter table public.devis add column if not exists date_echeance date;
alter table public.devis add column if not exists pdf_path text;

-- 2. Un numéro ne peut pas être utilisé deux fois pour une même entreprise
create unique index if not exists devis_numero_tenant_uniq
  on public.devis (tenant_id, numero)
  where numero is not null;

-- 3. Compteurs séquentiels par entreprise, par année, par type
create table if not exists public.document_counters (
  tenant_id      uuid not null references public.tenants(id) on delete cascade,
  annee          int  not null,
  type_document  text not null check (type_document in ('devis','facture')),
  dernier_numero int  not null default 0,
  primary key (tenant_id, annee, type_document)
);

alter table public.document_counters enable row level security;
-- Aucune policy : accès uniquement via la fonction ci-dessous (service_role).

-- 4. Numérotation atomique : DEV-2026-0001 / FAC-2026-0001, sans trou
create or replace function public.next_document_number(
  p_tenant uuid,
  p_type   text,
  p_annee  int
) returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  v_num  int;
  v_prefix text;
begin
  if p_type not in ('devis','facture') then
    raise exception 'Type de document invalide : %', p_type;
  end if;

  v_prefix := case when p_type = 'facture' then 'FAC' else 'DEV' end;

  insert into public.document_counters (tenant_id, annee, type_document, dernier_numero)
  values (p_tenant, p_annee, p_type, 1)
  on conflict (tenant_id, annee, type_document)
  do update set dernier_numero = public.document_counters.dernier_numero + 1
  returning dernier_numero into v_num;

  return v_prefix || '-' || p_annee::text || '-' || lpad(v_num::text, 4, '0');
end;
$$;

-- 5. Droits : la fonction est appelée par l'API (rôle service_role)
revoke all on function public.next_document_number(uuid, text, int) from public;
grant execute on function public.next_document_number(uuid, text, int) to service_role;
