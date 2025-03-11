# backend/api/system_router.py
from fastapi import APIRouter
from services.system_service import store_local_metrics, fetch_local_metrics
from utils.logger import log_info

router = APIRouter()

@router.post("/metrics/system/upload")
def upload_system_metrics():
    """Fetches and stores system metrics."""
    log_info("Uploading system metrics.")
    return store_local_metrics()

@router.get("/metrics/system")
def get_system_metrics(limit: int = 10):
    """Fetch latest system metrics."""
    log_info(f"Fetching latest {limit} system metrics.")
    return fetch_local_metrics(limit)