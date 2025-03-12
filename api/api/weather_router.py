from fastapi import APIRouter
from pydantic import BaseModel
from services.weather_service import store_weather_metrics, fetch_weather_metrics
from utils.logger import log_info

router = APIRouter()

class WeatherMetrics(BaseModel):
    temperature: float

@router.post("/metrics/weather/upload")
def upload_weather_metrics(metrics: WeatherMetrics):
    log_info("Receiving weather metrics from collector.")
    return store_weather_metrics(metrics.temperature)

@router.get("/metrics/weather")
def get_weather_metrics(limit: int = 10):
    log_info(f"Fetching latest {limit} weather metrics.")
    return fetch_weather_metrics(limit)