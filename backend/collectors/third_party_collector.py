import requests
from config.config import Config
from utils.logger import log_info, log_error

def fetch_weather_metric():
    """Fetches temperature from the weather API."""
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        raise ValueError("Missing weather API credentials")

    url = f"{Config.WEATHER_API_URL}?q=Dublin&appid={Config.WEATHER_API_KEY}"
    log_info("Fetching weather metric.")

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("main", {}).get("temp")
    except requests.RequestException as e:
        log_error(f"Weather API error: {e}")
        return None

def fetch_stock_metric():
    """Fetches stock price from the stock API."""
    if not Config.STOCK_API_URL or not Config.STOCK_API_KEY:
        raise ValueError("Missing stock API credentials")

    url = f"{Config.STOCK_API_URL}/AAPL/quote?token={Config.STOCK_API_KEY}"
    log_info("Fetching stock metric.")

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("latestPrice")
    except requests.RequestException as e:
        log_error(f"Stock API error: {e}")
        return None
