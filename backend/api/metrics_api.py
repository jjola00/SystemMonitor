from fastapi import APIRouter, HTTPException
from services.data_reporting import get_recent_metrics
from services.metrics_processing import store_external_metrics

router = APIRouter()

@router.get("/metrics")
def fetch_metrics(limit: int = 20):
    """Fetches the latest metrics, including device and third-party data."""
    try:
        return get_recent_metrics(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch-external-metrics")
def fetch_external():
    """Fetches and stores external metrics (weather & stock price)."""
    try:
        return store_external_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))