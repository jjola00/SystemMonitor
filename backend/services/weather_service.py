# backend/services/weather_service.py
from database.repositories.metric_repository import MetricRepository
from collectors.third_party_collector import fetch_weather_metric
from utils.logger import log_info

def store_weather_metrics():
    """Fetches and stores weather metrics."""
    metric_repo = MetricRepository()
    weather_temp = fetch_weather_metric()

    if weather_temp is not None:
        metric_repo.insert_weather_metric(weather_temp)
        log_info("Weather metrics stored successfully.")

def fetch_weather_metrics(limit=10):
    """Fetches latest weather metrics."""
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["weather_temp"], limit)