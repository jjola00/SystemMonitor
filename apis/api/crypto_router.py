from fastapi import APIRouter
from pydantic import BaseModel
from apis.services.crypto_service import store_crypto_metrics, fetch_crypto_metrics
from apis.utils.logger import log_info

router = APIRouter()

class CryptoMetrics(BaseModel):
    value: float
    unit: str

@router.post("/metrics/crypto/upload") #aggregator
def upload_crypto_metrics(metrics: CryptoMetrics):
    log_info("Receiving crypto metrics from collector.")
    return store_crypto_metrics(metrics.dict())

@router.get("/metrics/crypto") #reporter
def get_crypto_metrics(limit: int = 10):
    log_info(f"Fetching latest {limit} crypto metrics.")
    return fetch_crypto_metrics(limit)