import mimetypes, uuid
from django.conf import settings
from supabase import create_client

def _client():
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError('Supabase Storage is not configured.')
    return create_client(settings.SUPABASE_URL,settings.SUPABASE_SERVICE_ROLE_KEY)

def upload_private(uploaded_file,folder):
    ext=(uploaded_file.name.rsplit('.',1)[-1].lower() if '.' in uploaded_file.name else 'bin')
    path=f"{folder.strip('/')}/{uuid.uuid4().hex}.{ext}"
    content_type=uploaded_file.content_type or mimetypes.guess_type(uploaded_file.name)[0] or 'application/octet-stream'
    _client().storage.from_(settings.SUPABASE_STORAGE_BUCKET).upload(path,uploaded_file.read(),{'content-type':content_type,'upsert':'false'})
    return path

def signed_url(path,expires=600):
    if not path: return None
    result=_client().storage.from_(settings.SUPABASE_STORAGE_BUCKET).create_signed_url(path,expires)
    return result.get('signedURL') or result.get('signed_url')
