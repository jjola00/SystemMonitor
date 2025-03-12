import requests
from config.config import Config
from utils.logger import log_info, log_error

def fetch_weather_metric():
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        log_error("Missing weather API credentials.")
        return None
    params = {"location": "Dublin", "apikey": Config.WEATHER_API_KEY, "fields": ["temperature"], "units": "metric"}
    url = Config.WEATHER_API_URL
    log_info(f"Fetching weather metric from {url}")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "data" in data and "timelines" in data["data"]:
            timelines = data["data"]["timelines"]
            if timelines and "intervals" in timelines[0]:
                intervals = timelines[0]["intervals"]
                if intervals and "values" in intervals[0]:
                    return intervals[0]["values"].get("temperature")
        log_error("Temperature data not found in the response.")
        return None
    except requests.RequestException as e:
        log_error(f"Weather API error: {e}")
        return None

def fetch_crypto_metric():
    if not Config.CRYPTO_API_URL:
        log_error("Missing CoinGecko API credentials.")
        return None
    url = f"{Config.CRYPTO_API_URL}/simple/price?ids=bitcoin&vs_currencies=usd"
    log_info(f"Fetching crypto metric from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("bitcoin", {})
        if "usd" in data:
            return {"value": data["usd"], "unit": "USD"}
        log_error("Crypto API returned empty data.")
        return None
    except requests.RequestException as e:
        log_error(f"Crypto API error: {e}")
        return None