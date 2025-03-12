from ..database.db_connection import db_client
from datetime import datetime, timezone
from .device_repository import DeviceRepository
from utils.cache import cache
from utils.logger import log_info

class MetricRepository:
    def get_or_create_metric_id(self, metric_name, unit=None):
        cache_key = f"metric_id_{metric_name}"
        cached_id = cache.get(cache_key)
        if cached_id:
            return cached_id
        response = db_client.table("metrics").select("id").eq("name", metric_name).execute()
        if response.data:
            metric_id = response.data[0]["id"]
            cache.set(cache_key, metric_id, ttl_seconds=3600)
            return metric_id
        new_metric = {"name": metric_name, "unit": unit}
        insert_response = db_client.table("metrics").insert(new_metric).execute()
        if insert_response.data:
            metric_id = insert_response.data[0]["id"]
            cache.set(cache_key, metric_id, ttl_seconds=3600)
            return metric_id
        raise ValueError(f"Failed to create metric: {metric_name}")

    def insert_device_metrics(self, device_id, metrics):
        records = []
        for metric_name, value in metrics.items():
            if metric_name == "timestamp" or metric_name == "device_name":
                continue
            metric_id = self.get_or_create_metric_id(metric_name)
            records.append({
                "device_id": device_id,
                "metric_id": metric_id,
                "value": value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        if records:
            db_client.table("device_metrics").insert(records).execute()

    def insert_weather_metric(self, weather_temp):
        device_repo = DeviceRepository()
        metric_id = self.get_or_create_metric_id("weather_temp", unit="°C")
        device_id = device_repo.get_or_create_device_id("WeatherMonitor")
        db_client.table("device_metrics").insert([{
            "device_id": device_id,
            "metric_id": metric_id,
            "value": weather_temp,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]).execute()
        cache.delete("weather_metrics")

    def insert_crypto_metric(self, crypto_price):
        device_repo = DeviceRepository()
        metric_id = self.get_or_create_metric_id("crypto_price", unit="USD")
        device_id = device_repo.get_or_create_device_id("CryptoMonitor")
        db_client.table("device_metrics").insert([{
            "device_id": device_id,
            "metric_id": metric_id,
            "value": crypto_price["value"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]).execute()
        cache.delete("crypto_metrics")

    def fetch_metrics(self, metric_names, limit=10):
        log_info(f"Executing database query for metrics: {metric_names}")
        metric_ids_response = db_client.table("metrics") \
            .select("id") \
            .in_("name", metric_names) \
            .execute()
        if not metric_ids_response.data:
            return {"message": f"No metrics found for {metric_names}"}
        metric_ids = [item["id"] for item in metric_ids_response.data]
        response = db_client.table("device_metrics") \
            .select("value, timestamp, metrics(name)") \
            .in_("metric_id", metric_ids) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        return response.data or {"message": f"No metrics found for {metric_names}"}