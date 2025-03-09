from fastapi import APIRouter, HTTPException
from services.device_management import register_device, upload_metrics

router = APIRouter()

@router.post("/register-device")
def register(device_name: str, ip_address: str, location: str = "Unknown"):
    """Registers a new device in the database."""
    try:
        return register_device(device_name, ip_address, location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-metrics")
def upload(metrics: dict):
    """Uploads device metrics (CPU & RAM usage)."""
    try:
        return upload_metrics(metrics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
