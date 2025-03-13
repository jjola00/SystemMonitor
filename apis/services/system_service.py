from apis.database.repositories.device_repository import DeviceRepository
from apis.database.repositories.metric_repository import MetricRepository
from apis.utils.logger import log_info
from apis.utils.cache import cache
from apis.utils.cache_decorators import cached

def store_local_metrics(metrics: dict):
    device_repo = DeviceRepository()
    metric_repo = MetricRepository()
    device_id = device_repo.get_or_create_device_id(metrics["device_name"])
    metric_repo.insert_device_metrics(device_id, metrics)
    cache.delete("local_metrics")
    log_info("Local metrics stored successfully.")
    return {"status": "success"}

@cached(ttl_seconds=60, key_prefix="local_metrics")
def fetch_local_metrics(limit=30):  # Changed from 10 to 30
    log_info(f"Cache miss - fetching latest {limit} local metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["cpu_usage", "ram_usage"], limit)