# backend/database/repositories/metric_repository.py
from database.db_connection import db_client
from datetime import datetime, timezone
from .device_repository import DeviceRepository

class MetricRepository:
    def get_or_create_metric_id(self, metric_name, unit=None):
        """
        Fetch metric ID by name, or create it if it doesn't exist.
        If the metric doesn't exist, it will be created with the provided unit.
        """
        response = db_client.table("metrics").select("id").eq("name", metric_name).execute()
        
        if response.data:
            # Metric already exists, return its ID
            return response.data[0]["id"]
        
        # Metric doesn't exist, create it
        new_metric = {"name": metric_name, "unit": unit}
        insert_response = db_client.table("metrics").insert(new_metric).execute()
        
        if insert_response.data:
            return insert_response.data[0]["id"]
        else:
            raise ValueError(f"Failed to create metric: {metric_name}")

    def insert_device_metrics(self, device_id, metrics):
        """
        Insert device metrics into the database.
        metrics: A dictionary where keys are metric names and values are metric values.
        """
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
        """
        Insert weather metrics into the database.
        """
        device_repo = DeviceRepository()
        metric_id = self.get_or_create_metric_id("weather_temp", unit="°C")
        device_id = device_repo.get_or_create_device_id("WeatherMonitor")

        db_client.table("device_metrics").insert([
            {
                "device_id": device_id,
                "metric_id": metric_id,
                "value": weather_temp,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]).execute()

    def insert_crypto_metric(self, crypto_price):
        """
        Insert crypto metrics into the database.
        """
        device_repo = DeviceRepository()
        metric_id = self.get_or_create_metric_id("crypto_price", unit="USD")
        device_id = device_repo.get_or_create_device_id("CryptoMonitor")

        db_client.table("device_metrics").insert([
            {
                "device_id": device_id,
                "metric_id": metric_id,
                "value": crypto_price["value"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        ]).execute()

    def fetch_metrics(self, metric_names, limit=10):
        """
        Fetch latest metrics by names.
        """
        response = db_client.table("device_metrics") \
            .select("value, timestamp, metrics(name)") \
            .in_("metrics.name", metric_names) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        return response.data or {"message": f"No metrics found for {metric_names}"}