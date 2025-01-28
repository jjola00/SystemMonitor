import psutil
import requests

# Collect PC metrics
def get_pc_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage": psutil.virtual_memory().percent,
    }

# Collect third-party metrics (example: weather data)
def get_third_party_metrics():
    # Replace with an actual API for third-party data
    try:
        response = requests.get('https://api.weatherapi.com/v1/current.json', params={
            'key': 'your_weather_api_key',
            'q': 'Dublin'
        })
        data = response.json()
        return {
            "temperature": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
        }
    except Exception as e:
        return {"error": str(e)}
