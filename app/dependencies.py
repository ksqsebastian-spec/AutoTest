from supabase import Client

from app.db.client import get_supabase_client


def get_db() -> Client:
    """FastAPI dependency that provides the Supabase client."""
    return get_supabase_client()
