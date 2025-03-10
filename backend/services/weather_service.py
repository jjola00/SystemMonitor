# backend/services/weather_service.py
from database.repositories.metric_repository import MetricRepository
from collectors.third_party_collector import fetch_weather_metric
from utils.logger import log_info
from utils.cache import cache
from utils.cache_decorators import cached

def store_weather_metrics():
    """Fetches and stores weather metrics."""
    metric_repo = MetricRepository()
    weather_temp = fetch_weather_metric()

    if weather_temp is not None:
        metric_repo.insert_weather_metric(weather_temp)
        
        # Invalidate the cache after new data is stored
        cache.delete("weather_metrics")
        
        log_info("Weather metrics stored successfully.")
        return {"status": "success"}
    return {"status": "error", "message": "Failed to fetch weather data"}

@cached(ttl_seconds=300, key_prefix="weather_metrics")  # 5 minute cache for weather
def fetch_weather_metrics(limit=10):
    """Fetches latest weather metrics with caching."""
    log_info(f"Cache miss - fetching latest {limit} weather metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["weather_temp"], limit)