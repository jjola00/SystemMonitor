from supabase import create_client, Client
from config.config import Config 

db_client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)