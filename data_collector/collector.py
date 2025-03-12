import requests
import time
import os
from collectors.system_collector import collect_system_metrics
from collectors.third_party_collector import fetch_weather_metric, fetch_crypto_metric
from utils.logger import log_info, log_error
from apis.config.config import Config

CLOUD_API_URL = "http://localhost:10000/api"
DEVICE_NAME = "test"

def send_metrics_to_cloud(endpoint, data):
    try:
        response = requests.post(f"{CLOUD_API_URL}/{endpoint}", json=data)
        response.raise_for_status()
        log_info(f"Successfully sent data to {endpoint}: {response.json()}")
    except requests.RequestException as e:
        log_error(f"Failed to send data to {endpoint}: {e}")

def fetch_and_execute_commands():
    try:
        response = requests.get(f"{CLOUD_API_URL}/command/{DEVICE_NAME}")
        response.raise_for_status()
        data = response.json()
        log_info(f"Received response from API: {data}")  # Add this
        command = data.get("command")
        if command == "open_task_manager":
            log_info("Executing command: open_task_manager")
            os.system("taskmgr")
        elif command:
            log_info(f"Unknown command received: {command}")
        else:
            log_info("No new commands to execute")
    except requests.RequestException as e:
        log_error(f"Failed to fetch commands: {e}")

def main():
    while True:
        # Send metrics
        system_metrics = collect_system_metrics()
        if system_metrics:
            send_metrics_to_cloud("metrics/system/upload", system_metrics)

        weather_temp = fetch_weather_metric()
        if weather_temp is not None:
            send_metrics_to_cloud("metrics/weather/upload", {"temperature": weather_temp})

        crypto_price = fetch_crypto_metric()
        if crypto_price is not None:
            send_metrics_to_cloud("metrics/crypto/upload", crypto_price)

        # Fetch and execute commands
        fetch_and_execute_commands()

        time.sleep(5)  # Keep at 5s for responsiveness

if __name__ == "__main__":
    Config.validate()
    main()