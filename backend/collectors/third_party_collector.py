import requests
from config.config import Config

def fetch_weather_metric(location="Dublin"):
    """Fetches temperature data from a weather API."""
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        raise ValueError("Weather API credentials are missing")

    response = requests.get(f"{Config.WEATHER_API_URL}?q={location}&appid={Config.WEATHER_API_KEY}")
    if response.status_code == 200:
        return response.json()["main"]["temp"]
    raise ValueError(f"Failed to fetch weather data: {response.status_code}")

def fetch_stock_metric(symbol="AAPL"):
    """Fetches stock price data from a stock market API."""
    if not Config.STOCK_API_URL or not Config.STOCK_API_KEY:
        raise ValueError("Stock API credentials are missing")

    response = requests.get(f"{Config.STOCK_API_URL}/{symbol}/quote?token={Config.STOCK_API_KEY}")
    if response.status_code == 200:
        return response.json()["latestPrice"]
    raise ValueError(f"Failed to fetch stock data: {response.status_code}")
