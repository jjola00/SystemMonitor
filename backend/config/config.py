#backend/config/config.py
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

    # Weather API Credentials
    WEATHER_API_URL = os.getenv("WEATHER_API_URL")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

    # Stock API Credentials
    STOCK_API_URL = os.getenv("STOCK_API_URL")
    STOCK_API_KEY = os.getenv("STOCK_API_KEY")

    @staticmethod
    def validate():
        """Ensure critical configs are set."""
        missing = [key for key in ["SUPABASE_URL", "SUPABASE_KEY", "AGGREGATOR_API", "WEATHER_API_URL", "WEATHER_API_KEY", "STOCK_API_URL", "STOCK_API_KEY"] if not getattr(Config, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Validate configuration at runtime
Config.validate()