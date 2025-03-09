from fastapi import APIRouter, HTTPException
from services.data_ingestion import store_metrics, fetch_metrics
from services.metrics_processing import get_third_party_metrics

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
        return get_third_party_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
