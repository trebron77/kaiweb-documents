-- Étend la numérotation aux procès-verbaux (PV) et commandes (CMD).
-- À exécuter dans Supabase → SQL Editor, APRÈS 2026-11-21_types_documents.sql.

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
  if p_type not in ('devis','facture','pv','commande') then
    raise exception 'Type de document invalide : %', p_type;
  end if;

  v_prefix := case p_type
    when 'facture'  then 'FAC'
    when 'pv'       then 'PV'
    when 'commande' then 'CMD'
    else 'DEV'
  end;

  insert into public.document_counters (tenant_id, annee, type_document, dernier_numero)
  values (p_tenant, p_annee, p_type, 1)
  on conflict (tenant_id, annee, type_document)
  do update set dernier_numero = public.document_counters.dernier_numero + 1
  returning dernier_numero into v_num;

  return v_prefix || '-' || p_annee::text || '-' || lpad(v_num::text, 4, '0');
end;
$$;

revoke all on function public.next_document_number(uuid, text, int) from public;
grant execute on function public.next_document_number(uuid, text, int) to service_role;
