# backend/api/routers/crypto_router.py
from fastapi import APIRouter
from services.crypto_service import store_crypto_metrics, fetch_crypto_metrics
from utils.logger import log_info

router = APIRouter()

@router.post("/metrics/crypto/upload")
def upload_crypto_metrics():
    """Fetches and stores crypto metrics."""
    log_info("Uploading crypto metrics.")
    return store_crypto_metrics()

@router.get("/metrics/crypto")
def get_crypto_metrics(limit: int = 10):
    """Fetch latest crypto metrics."""
    log_info(f"Fetching latest {limit} crypto metrics.")
    return fetch_crypto_metrics(limit)