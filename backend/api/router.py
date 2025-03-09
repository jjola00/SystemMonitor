from fastapi import APIRouter, HTTPException
from services.device_management import register_device, upload_metrics, store_metrics, store_external_metrics
from services.metrics_service import fetch_metrics, get_recent_metrics

router = APIRouter()

@router.post("/upload")
def upload_metrics(metrics: dict):
    try:
        store_metrics(metrics)
        return {"message": "Metrics stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
def get_metrics():
    try:
        return fetch_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/third-party")
def third_party_metrics():
    try:
        return store_external_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register-device")
def register(device_name: str, ip_address: str, location: str = "Unknown"):
    """Registers a new device in the database."""
    try:
        return register_device(device_name, ip_address, location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/metrics/upload")
def upload(metrics: dict):
    """Uploads device metrics (CPU & RAM usage)."""
    try:
        return upload_metrics(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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
