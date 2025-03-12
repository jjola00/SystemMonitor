from database.repositories.metric_repository import MetricRepository
from utils.logger import log_info
from utils.cache import cache
from utils.cache_decorators import cached

def store_weather_metrics(temperature: float):
    metric_repo = MetricRepository()
    metric_repo.insert_weather_metric(temperature)
    cache.delete("weather_metrics")
    log_info("Weather metrics stored successfully.")
    return {"status": "success"}

@cached(ttl_seconds=300, key_prefix="weather_metrics")
def fetch_weather_metrics(limit=10):
    log_info(f"Cache miss - fetching latest {limit} weather metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["weather_temp"], limit)