# backend/services/system_service.py
from database.repositories.device_repository import DeviceRepository
from database.repositories.metric_repository import MetricRepository
from collectors.system_collector import collect_system_metrics
from utils.logger import log_info
from fastapi import HTTPException

def store_local_metrics():
    """Fetches and stores CPU and RAM usage."""
    metrics = collect_system_metrics()
    
    if metrics is not None:
        device_repo = DeviceRepository()
        metric_repo = MetricRepository()
        
        device_id = device_repo.get_or_create_device_id(metrics["device_name"])
        
        metric_repo.insert_device_metrics(device_id, metrics)
        log_info("Local metrics stored successfully.")
        return {"status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Failed to collect system metrics")    

def fetch_local_metrics(limit=10):
    """Fetches latest local device metrics."""
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["cpu_usage", "ram_usage"], limit)