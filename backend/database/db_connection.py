import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load secrets
load_dotenv("backend/config/secrets.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not set in environment variables.")

db_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
