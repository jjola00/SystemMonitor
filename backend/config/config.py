import os
from dotenv import load_dotenv

# Load environment variables from secrets.env
env_path = os.path.join(os.path.dirname(__file__), "secrets.env")
load_dotenv(env_path)

class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    AGGREGATOR_API = os.getenv("AGGREGATOR_API")
    DEVICE_NAME = os.getenv("DEVICE_NAME", "Unnamed Device")

    METRIC_COLLECTION_INTERVAL = int(os.getenv("METRIC_COLLECTION_INTERVAL", 5))  # Default: 5 seconds
    THIRD_PARTY_API_URL = os.getenv("THIRD_PARTY_API_URL")  # API for external data (e.g., weather, stock prices)

    @staticmethod
    def validate():
        """Ensure critical configs are set."""
        missing = [key for key in ["SUPABASE_URL", "SUPABASE_KEY", "AGGREGATOR_API"] if not getattr(Config, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate configuration at runtime
Config.validate()