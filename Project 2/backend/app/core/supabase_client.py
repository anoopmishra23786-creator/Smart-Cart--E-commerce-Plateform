from typing import Optional
from supabase import create_client, Client
from backend.app.core.config import settings

_supabase_anon: Optional[Client] = None
_supabase_admin: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """Returns anonymous Supabase client for safe public queries."""
    global _supabase_anon
    if _supabase_anon is None and settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
        try:
            _supabase_anon = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
        except Exception:
            _supabase_anon = None
    return _supabase_anon

def get_supabase_admin_client() -> Optional[Client]:
    """
    Returns privileged Supabase client using service role key.
    MUST only be accessed server-side after strict identity & authorization checks!
    """
    global _supabase_admin
    if _supabase_admin is None and settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
        try:
            _supabase_admin = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        except Exception:
            _supabase_admin = None
    return _supabase_admin
