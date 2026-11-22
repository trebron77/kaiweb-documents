-- Ajoute les types « pv » (procès-verbal de chantier) et « commande »
-- (commande de matériaux) aux compteurs de documents.
--
-- À exécuter dans Supabase → SQL Editor.

alter table public.document_counters
  drop constraint if exists document_counters_type_document_check;

alter table public.document_counters
  add constraint document_counters_type_document_check
  check (type_document in ('devis', 'facture', 'pv', 'commande'));

-- Vérification : la contrainte doit lister les quatre types.
select conname, pg_get_constraintdef(oid) as definition
from pg_constraint
where conrelid = 'public.document_counters'::regclass
  and conname = 'document_counters_type_document_check';
