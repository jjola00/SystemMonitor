# backend/api/routers/weather_router.py
from fastapi import APIRouter
from services.weather_service import store_weather_metrics, fetch_weather_metrics
from utils.logger import log_info

router = APIRouter()

@router.post("/metrics/weather/upload")
def upload_weather_metrics():
    """Fetches and stores weather metrics."""
    log_info("Uploading weather metrics.")
    return store_weather_metrics()

@router.get("/metrics/weather")
def get_weather_metrics(limit: int = 10):
    """Fetch latest weather metrics."""
    log_info(f"Fetching latest {limit} weather metrics.")
    return fetch_weather_metrics(limit)