from database.db_connection import db_client
from datetime import datetime

def store_metrics(metrics: dict):
    device_name = metrics.get("device_name")
    cpu_usage = metrics.get("cpu_usage")
    ram_usage = metrics.get("ram_usage")

    if not device_name or cpu_usage is None or ram_usage is None:
        raise ValueError("Missing required fields: device_name, cpu_usage, ram_usage")

    device_response = db_client.table("devices").select("id").eq("name", device_name).execute()
    if device_response.data:
        device_id = device_response.data[0]["id"]
    else:
        device_response = db_client.table("devices").insert({
            "name": device_name,
            "ip_address": "unknown",
            "location": "unknown",
            "created_at": datetime.utcnow()
        }).execute()
        device_id = device_response.data[0]["id"]

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["cpu_usage", "ram_usage"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "cpu_usage" not in metric_map or "ram_usage" not in metric_map:
        raise ValueError("Metrics (cpu_usage, ram_usage) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": cpu_usage, "timestamp": datetime.utcnow()},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": ram_usage, "timestamp": datetime.utcnow()},
    ]).execute()

def fetch_metrics():
    response = db_client.table("device_metrics") \
        .select("value, timestamp, devices(name), metrics(name, unit)") \
        .order("timestamp", desc=True) \
        .limit(20) \
        .execute()

    if not response.data:
        return []

    return [
        {
            "device_name": row["devices"]["name"],
            "metric_name": row["metrics"]["name"],
            "value": row["value"],
            "unit": row["metrics"]["unit"],
            "timestamp": row["timestamp"]
        }
        for row in response.data
    ]
