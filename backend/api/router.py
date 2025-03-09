from fastapi import APIRouter, HTTPException
from services.device_management import register_device, upload_metrics, store_metrics, store_external_metrics
from services.metrics_service import fetch_metrics, get_recent_metrics
from utils.logger import log_info, log_error

router = APIRouter()

@router.post("/upload")
def upload_metrics(metrics: dict):
    try:
        log_info("Uploading metrics.")
        store_metrics(metrics)
        log_info("Metrics stored successfully.")
        return {"message": "Metrics stored successfully"}
    except Exception as e:
        log_error(f"Error storing metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
def get_metrics():
    try:
        log_info("Fetching metrics.")
        return fetch_metrics()
    except Exception as e:
        log_error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/third-party")
def third_party_metrics():
    try:
        log_info("Fetching third-party metrics.")
        return store_external_metrics()
    except Exception as e:
        log_error(f"Error fetching third-party metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register-device")
def register(device_name: str, ip_address: str, location: str = "Unknown"):
    try:
        log_info(f"Registering device: {device_name}, IP: {ip_address}, Location: {location}")
        return register_device(device_name, ip_address, location)
    except Exception as e:
        log_error(f"Error registering device: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/metrics/upload")
def upload(metrics: dict):
    try:
        log_info("Uploading device metrics.")
        return upload_metrics(metrics)
    except Exception as e:
        log_error(f"Error uploading device metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
def fetch_metrics(limit: int = 20):
    try:
        log_info(f"Fetching latest metrics with limit: {limit}.")
        return get_recent_metrics(limit)
    except Exception as e:
        log_error(f"Error fetching latest metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fetch-external-metrics")
def fetch_external():
    try:
        log_info("Fetching external metrics.")
        return store_external_metrics()
    except Exception as e:
        log_error(f"Error fetching external metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))