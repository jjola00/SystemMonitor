import requests
from config.config import Config
from utils.logger import log_info, log_error

def fetch_weather_metric():
    """Fetches temperature from the weather API."""
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        log_error("Missing weather API credentials.")
        return None

    # Define the parameters for the API request
    params = {
        "location": "Dublin",  # Specify the location
        "apikey": Config.WEATHER_API_KEY,  # Your API key
        "fields": ["temperature"],  # Specify the fields you want to retrieve
        "units": "metric"  # Specify the unit (metric for Celsius, imperial for Fahrenheit)
    }

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
                    temperature = intervals[0]["values"].get("temperature")
                    return temperature

        log_error("Temperature data not found in the response.")
        return None
    except requests.RequestException as e:
        log_error(f"Weather API error: {e}")
        return None

def fetch_crypto_metric():
    """Fetches Bitcoin price from CoinGecko and includes the unit."""
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
