from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction


EXCLUDED_TABLES = {"spatial_ref_sys"}


class Command(BaseCommand):
    help = (
        "Enable Row Level Security on public PostgreSQL tables and revoke "
        "Supabase Data API access from anon/authenticated roles."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--check",
            action="store_true",
            help="Only report current RLS status; do not change anything.",
        )

    def handle(self, *args, **options):
        if connection.vendor != "postgresql":
            raise CommandError(
                "This command only works with PostgreSQL/Supabase. "
                "Add the Supabase DATABASE_URL to .env first."
            )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename
                """
            )
            tables = [row[0] for row in cursor.fetchall() if row[0] not in EXCLUDED_TABLES]

        if not tables:
            self.stdout.write(self.style.WARNING("No public tables were found."))
            return

        if not options["check"]:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    for table in tables:
                        quoted = connection.ops.quote_name(table)
                        cursor.execute(f"ALTER TABLE public.{quoted} ENABLE ROW LEVEL SECURITY")
                        cursor.execute(f"REVOKE ALL ON TABLE public.{quoted} FROM anon")
                        cursor.execute(f"REVOKE ALL ON TABLE public.{quoted} FROM authenticated")

                    cursor.execute("REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon")
                    cursor.execute("REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM authenticated")
                    cursor.execute("REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM anon")
                    cursor.execute("REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM authenticated")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Secured {len(tables)} public tables. Django's direct PostgreSQL "
                    "connection continues to work; Supabase anon/authenticated Data API access is blocked."
                )
            )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT c.relname, c.relrowsecurity
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = 'public'
                  AND c.relkind = 'r'
                ORDER BY c.relname
                """
            )
            rows = [(name, enabled) for name, enabled in cursor.fetchall() if name not in EXCLUDED_TABLES]

        enabled_count = sum(1 for _, enabled in rows if enabled)
        self.stdout.write(f"RLS enabled: {enabled_count}/{len(rows)} tables")
        for name, enabled in rows:
            marker = "OK" if enabled else "NOT ENABLED"
            style = self.style.SUCCESS if enabled else self.style.ERROR
            self.stdout.write(style(f"  {marker:11} {name}"))
