import requests
from config.config import Config
from utils.logger import log_info, log_error

def fetch_weather_metric(location="Dublin"):
    """Fetches temperature data from a weather API."""
    if not Config.WEATHER_API_URL or not Config.WEATHER_API_KEY:
        raise ValueError("Weather API credentials are missing")

    log_info(f"Fetching weather metric for location: {location}")
    response = requests.get(f"{Config.WEATHER_API_URL}?q={location}&appid={Config.WEATHER_API_KEY}")
    if response.status_code == 200:
        log_info("Weather data fetched successfully.")
        return response.json()["main"]["temp"]
    log_error(f"Failed to fetch weather data: {response.status_code}")
    raise ValueError(f"Failed to fetch weather data: {response.status_code}")

def fetch_stock_metric(symbol="AAPL"):
    """Fetches stock price data from a stock market API."""
    if not Config.STOCK_API_URL or not Config.STOCK_API_KEY:
        raise ValueError("Stock API credentials are missing")

    log_info(f"Fetching stock metric for symbol: {symbol}")
    response = requests.get(f"{Config.STOCK_API_URL}/{symbol}/quote?token={Config.STOCK_API_KEY}")
    if response.status_code == 200:
        log_info("Stock data fetched successfully.")
        return response.json()["latestPrice"]
    log_error(f"Failed to fetch stock data: {response.status_code}")
    raise ValueError(f"Failed to fetch stock data: {response.status_code}")
