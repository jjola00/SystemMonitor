# backend/database/repositories/metric_repository.py
from database.db_connection import db_client
from datetime import datetime, timezone

class MetricRepository:
    def get_metric_ids(self, metric_names):
        """Fetch metric IDs by names."""
        response = db_client.table("metrics").select("id, name").in_("name", metric_names).execute()
        return {m["name"]: m["id"] for m in response.data}

    def insert_device_metrics(self, device_id, metric_map, metrics):
        """Insert device metrics into the database."""
        db_client.table("device_metrics").insert([
            {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": metrics["cpu_usage"], "timestamp": datetime.now(timezone.utc).isoformat()},
            {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": metrics["ram_usage"], "timestamp": datetime.now(timezone.utc).isoformat()}
        ]).execute()

    def fetch_metrics(self, metric_names, limit=10):
        """Fetch latest metrics by names."""
        response = db_client.table("device_metrics") \
            .select("value, timestamp, metrics(name)") \
            .in_("metrics.name", metric_names) \
            .order("timestamp", desc=True) \
            .limit(limit) \
            .execute()
        return response.data or {"message": f"No metrics found for {metric_names}"}