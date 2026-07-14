from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('SECRET_KEY', 'development-only-change-me')
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [u.strip() for u in os.getenv('CSRF_TRUSTED_ORIGINS','').split(',') if u.strip()]

INSTALLED_APPS = [
 'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
 'django.contrib.messages','django.contrib.staticfiles',
 'core','accounts','leave_management','claims','communications','attendance','audit','payroll','vouchers','maintenance','notifications',
]
MIDDLEWARE = [
 'django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware',
 'audit.middleware.AuditMiddleware',
]
ROOT_URLCONF='config.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,
'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','notifications.context_processors.notification_summary']}}]
WSGI_APPLICATION='config.wsgi.application'
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=60,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
AUTH_USER_MODEL='accounts.User'
AUTH_PASSWORD_VALIDATORS=[
 {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
 {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':10}},
 {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
 {'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE='en-gb'; TIME_ZONE='Asia/Kuching'; USE_I18N=True; USE_TZ=True
STATIC_URL='/static/'; STATIC_ROOT=BASE_DIR/'staticfiles'; STATICFILES_DIRS=[BASE_DIR/'static']
STORAGES={'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG else 'whitenoise.storage.CompressedManifestStaticFilesStorage'}}
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='login'; LOGIN_REDIRECT_URL='dashboard'; LOGOUT_REDIRECT_URL='login'
SESSION_COOKIE_HTTPONLY=True; SESSION_COOKIE_SAMESITE='Lax'; CSRF_COOKIE_SAMESITE='Lax'
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO','https')
if not DEBUG:
    SESSION_COOKIE_SECURE=True; CSRF_COOKIE_SECURE=True; SECURE_SSL_REDIRECT=os.getenv('SECURE_SSL_REDIRECT','1')=='1'
SUPABASE_URL=os.getenv('SUPABASE_URL','').rstrip('/')
SUPABASE_SERVICE_ROLE_KEY=os.getenv('SUPABASE_SERVICE_ROLE_KEY','')
SUPABASE_STORAGE_BUCKET=os.getenv('SUPABASE_STORAGE_BUCKET','hr-private')
FILE_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024
DATA_UPLOAD_MAX_MEMORY_SIZE=12*1024*1024
