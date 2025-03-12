from fastapi import APIRouter
from pydantic import BaseModel
from services.system_service import store_local_metrics, fetch_local_metrics
from utils.logger import log_info

router = APIRouter()

class SystemMetrics(BaseModel):
    device_name: str
    cpu_usage: float
    ram_usage: float
    timestamp: str

@router.post("/metrics/system/upload")
def upload_system_metrics(metrics: SystemMetrics):
    log_info("Receiving system metrics from collector.")
    return store_local_metrics(metrics.dict())

@router.get("/metrics/system")
def get_system_metrics(limit: int = 10):
    log_info(f"Fetching latest {limit} system metrics.")
    return fetch_local_metrics(limit)