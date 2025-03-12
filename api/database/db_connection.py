from supabase import create_client, Client
from config.config import Config

try:
    db_client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
except Exception as e:
    raise RuntimeError(f"Database connection failed: {e}")