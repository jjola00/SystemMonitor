import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), "secrets.env")
load_dotenv(env_path)

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    AGGREGATOR_API = os.getenv("AGGREGATOR_API")
    DEVICE_NAME = os.getenv("DEVICE_NAME", "Unnamed Device")

    @staticmethod
    def validate():
        missing = [key for key in ["SUPABASE_URL", "SUPABASE_KEY", "AGGREGATOR_API"] if not getattr(Config, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

Config.validate()