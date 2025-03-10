# backend/api/routers/system_router.py
from fastapi import APIRouter
from services.system_service import store_local_metrics, fetch_local_metrics
from utils.logger import log_info

router = APIRouter()

@router.post("/metrics/upload")
def upload_device_metrics(metrics: dict):
    """Collects and stores local device metrics."""
    log_info("Uploading local device metrics.")
    return store_local_metrics(metrics)

@router.get("/metrics/local")
def get_local_metrics(limit: int = 20):
    """Fetch latest local device metrics."""
    log_info(f"Fetching latest {limit} local metrics.")
    return fetch_local_metrics(limit)