from supabase import Client
from supabase import create_client

from app.core.config import settings


def get_supabase_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_key)

def get_supabase_service_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_key)
