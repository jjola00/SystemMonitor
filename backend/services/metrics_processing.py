import requests
from datetime import datetime
from database.db_connection import db_client
from config.config import Config 

def fetch_weather_metric(location="Dublin"):
    """Fetches temperature data from a weather API."""
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        raise ValueError("Weather API credentials are missing")

    response = requests.get(f"{Config.WEATHER_API_URL}?q={location}&appid={Config.WEATHER_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        return data["main"]["temp"]
    else:
        raise ValueError(f"Failed to fetch weather data: {response.status_code}")

def fetch_stock_metric(symbol="AAPL"):
    """Fetches stock price data from a stock market API."""
    if not Config.STOCK_API_URL or not Config.STOCK_API_KEY:
        raise ValueError("Stock API credentials are missing")

    response = requests.get(f"{Config.STOCK_API_URL}/{symbol}/quote?token={Config.STOCK_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        return data["latestPrice"]
    else:
        raise ValueError(f"Failed to fetch stock data: {response.status_code}")

def store_external_metrics():
    """Fetches and stores third-party metrics (weather and stock price)."""
    weather_value = fetch_weather_metric()
    stock_value = fetch_stock_metric()

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["weather_temp", "stock_price"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "weather_temp" not in metric_map or "stock_price" not in metric_map:
        raise ValueError("Metrics (weather_temp, stock_price) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": None, "metric_id": metric_map["weather_temp"], "value": weather_value, "timestamp": datetime.utcnow()},
        {"device_id": None, "metric_id": metric_map["stock_price"], "value": stock_value, "timestamp": datetime.utcnow()},
    ]).execute()

    return {"weather_temp": weather_value, "stock_price": stock_value}