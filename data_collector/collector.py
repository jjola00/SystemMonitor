import requests
import time
from collectors.system_collector import collect_system_metrics
from collectors.third_party_collector import fetch_weather_metric, fetch_crypto_metric
from utils.logger import log_info, log_error
from config.config import Config

# Default to local API for testing; update to deployed URL later
CLOUD_API_URL = "http://localhost:10000/api"

def send_metrics_to_cloud(endpoint, data):
    try:
        response = requests.post(f"{CLOUD_API_URL}/{endpoint}", json=data)
        response.raise_for_status()
        log_info(f"Successfully sent data to {endpoint}: {response.json()}")
    except requests.RequestException as e:
        log_error(f"Failed to send data to {endpoint}: {e}")

def main():
    while True:
        system_metrics = collect_system_metrics()
        if system_metrics:
            send_metrics_to_cloud("metrics/system/upload", system_metrics)

        weather_temp = fetch_weather_metric()
        if weather_temp is not None:
            send_metrics_to_cloud("metrics/weather/upload", {"temperature": weather_temp})

        crypto_price = fetch_crypto_metric()
        if crypto_price is not None:
            send_metrics_to_cloud("metrics/crypto/upload", crypto_price)

        time.sleep(60)

if __name__ == "__main__":
    Config.validate()
    main()