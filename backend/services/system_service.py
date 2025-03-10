# backend/services/system_service.py
from database.repositories.device_repository import DeviceRepository
from database.repositories.metric_repository import MetricRepository
from collectors.system_collector import collect_system_metrics
from utils.logger import log_info
from fastapi import HTTPException
from utils.cache import cache
from utils.cache_decorators import cached

def store_local_metrics():
    """Fetches and stores CPU and RAM usage."""
    metrics = collect_system_metrics()
    
    if metrics is not None:
        device_repo = DeviceRepository()
        metric_repo = MetricRepository()
        
        device_id = device_repo.get_or_create_device_id(metrics["device_name"])
        
        metric_repo.insert_device_metrics(device_id, metrics)
        
        # Invalidate the cache after new data is stored
        cache.delete("local_metrics")
        
        log_info("Local metrics stored successfully.")
        return {"status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Failed to collect system metrics")    

@cached(ttl_seconds=60, key_prefix="local_metrics")
def fetch_local_metrics(limit=10):
    """Fetches latest local device metrics with caching."""
    log_info(f"Cache miss - fetching latest {limit} local metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["cpu_usage", "ram_usage"], limit)