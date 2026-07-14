-- JETAMA PeopleOS / Django + Supabase security hardening
-- Run after: python manage.py migrate
--
-- The Django server connects directly to PostgreSQL using DATABASE_URL.
-- The browser does not access HR tables through the Supabase Data API.
-- Therefore, public tables can safely have RLS enabled with no anon/authenticated policies.

DO $$
DECLARE
    table_record RECORD;
BEGIN
    FOR table_record IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
          AND tablename <> 'spatial_ref_sys'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', table_record.tablename);
        EXECUTE format('REVOKE ALL ON TABLE public.%I FROM anon', table_record.tablename);
        EXECUTE format('REVOKE ALL ON TABLE public.%I FROM authenticated', table_record.tablename);
    END LOOP;
END $$;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM authenticated;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM anon;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM authenticated;

-- Confirm RLS state.
SELECT
    c.relname AS table_name,
    c.relrowsecurity AS rls_enabled
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relkind = 'r'
ORDER BY c.relname;
