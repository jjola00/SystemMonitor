from fastapi import APIRouter, HTTPException, Depends
from services.metrics_service import (
    store_local_metrics, 
    store_external_metrics, 
    fetch_local_metrics, 
    fetch_weather_metrics, 
    fetch_stock_metrics
)
from utils.logger import log_info

router = APIRouter()

@router.post("/metrics/upload")
def upload_device_metrics(metrics: dict):
    """Collects and stores local device metrics."""
    log_info("Uploading local device metrics.")
    return store_local_metrics(metrics)

@router.post("/metrics/fetch-external")
def fetch_external(metrics: dict):
    """Fetches and stores weather and stock metrics."""
    log_info("Fetching and storing external metrics.")
    return store_external_metrics(metrics)

@router.get("/metrics/local")
def get_local_metrics(limit: int = 20):
    """Fetch latest local device metrics."""
    log_info(f"Fetching latest {limit} local metrics.")
    return fetch_local_metrics(limit)

@router.get("/metrics/weather")
def get_weather_metrics(limit: int = 10):
    """Fetch latest weather temperature data."""
    log_info(f"Fetching latest {limit} weather metrics.")
    return fetch_weather_metrics(limit)

@router.get("/metrics/stocks")
def get_stock_metrics(limit: int = 10):
    """Fetch latest stock price data."""
    log_info(f"Fetching latest {limit} stock metrics.")
    return fetch_stock_metrics(limit)
