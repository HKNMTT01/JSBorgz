# JETAMA HR & ESG Management System

A clean Django foundation for employee management, leave, claims, notices, policies, private HR documents, approvals and audit logging.

## Architecture

- Django 5.2 LTS with server-rendered templates
- Supabase PostgreSQL through `DATABASE_URL`
- Private Supabase Storage with short-lived signed URLs
- Django authentication, groups/roles, password hashing, forms, migrations and admin
- WhiteNoise for static assets
- Gunicorn deployment on Render or Railway

## Included workflows

- Employees and departments
- Roles: Administrator, Employee, Supervisor, Manager, GM HR & ESG, GM Finance and CEO
- Leave applications with working-day calculation, entitlement validation, recommender and approver stages
- Claims: HR verification → Finance check → CEO approval
- Notices and policy documents
- Private receipts, supporting documents and policies
- Audit records for write operations
- Health endpoint at `/health/`

## Local setup on Windows

```powershell
cd "C:\path\to\jetama_hr_django"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py bootstrap_hr --email "your-email@example.com" --password "ChangeMe123!"
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

SQLite is used locally when `DATABASE_URL` is empty. Add the Supabase Transaction Pooler URI to `.env` when ready.

## Supabase setup

1. Create a Supabase project.
2. In **Connect**, copy the Transaction Pooler URI and assign it to `DATABASE_URL`.
3. In Storage, create a **private** bucket named `hr-private`.
4. Copy the project URL and server-side service-role key into `.env`.
5. Run `python manage.py migrate`; Django creates the tables in Supabase.
6. Run `python manage.py bootstrap_hr ...` to create the first administrator.

Do not run a separate `schema.sql`; Django migrations are the database source of truth.


## Supabase table security (remove `UNRESTRICTED`)

After migrations have created the tables in Supabase, run:

```powershell
python manage.py secure_supabase
```

This enables Row Level Security on all public tables and revokes Supabase Data API access from the `anon` and `authenticated` roles. The Django backend continues to access PostgreSQL through `DATABASE_URL`. Verify at any time with:

```powershell
python manage.py secure_supabase --check
```

You can also run `supabase_security.sql` in the Supabase SQL Editor. See `SECURITY.md` for the security model and production checklist.

## GitHub

```powershell
git init
git add .
git commit -m "Initial Django HR system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

`.env`, local databases and virtual environments are ignored.

## Render

The repository includes `render.yaml` and `build.sh`.

Set these environment variables:

- `DEBUG=0`
- `ALLOWED_HOSTS=your-service.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://your-service.onrender.com`
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_STORAGE_BUCKET=hr-private`

After deployment, open the Render Shell and run:

```bash
python manage.py bootstrap_hr --email you@example.com --password 'A-Strong-Password'
```

## Railway

The repository includes `railway.json`. Connect the GitHub repository, add the same environment variables, and deploy. Migrations and static collection run as the pre-deploy command.

## Before company production use

- Use a paid hosting/database plan with backups and point-in-time recovery.
- Configure company SMTP and password reset emails.
- Add MFA/SSO if required by company policy.
- Review role assignments and approval delegation.
- Add retention rules for medical and claim documents.
- Add automated tests for every approval and payroll-related workflow.
- Complete security and privacy review before importing real employee records.


## ERP UI upgrade
This edition includes a responsive PeopleOS design system, role-aware dashboards, attendance management, employee profiles, analytics reports and modern reusable form/table components. The shared Figma community file was used only as visual direction; the implementation is original and tailored to JETAMA workflows.
