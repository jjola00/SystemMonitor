from database.db_connection import db_client
from datetime import datetime, timezone
from collectors.system_collector import collect_system_metrics
from collectors.third_party_collector import fetch_weather_metric, fetch_stock_metric
from utils.logger import log_info, log_error
from fastapi import HTTPException

def get_or_create_device_id(device_name, ip_address=None):
    """Fetch device ID by name, or insert it if not found."""
    response = db_client.table("devices").select("id").eq("name", device_name).execute()
    
    if response.data:
        return response.data[0]["id"]
    
    new_device = {"name": device_name, "ip_address": ip_address, "created_at": datetime.utcnow()}
    insert_response = db_client.table("devices").insert(new_device).execute()
    
    return insert_response.data[0]["id"] if insert_response.data else None

def store_local_metrics():
    """Fetches and stores CPU and RAM usage."""
    metrics = collect_system_metrics()
    device_id = get_or_create_device_id(metrics["device_name"])

    # Fetch metric IDs
    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["cpu_usage", "ram_usage"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "cpu_usage" not in metric_map or "ram_usage" not in metric_map:
        raise HTTPException(status_code=500, detail="Metrics (cpu_usage, ram_usage) not found in database")

    # Insert metrics into device_metrics
    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": metrics["cpu_usage"], "timestamp": datetime.now(timezone.utc).isoformat()},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": metrics["ram_usage"], "timestamp": datetime.now(timezone.utc).isoformat()}
    ]).execute()

    log_info("Local metrics stored successfully.")

def store_external_metrics():
    """Fetches and stores weather and stock metrics."""
    device_name = "Server 1"  # Define a consistent device name
    device_id = get_or_create_device_id(device_name)

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["weather_temp", "stock_price"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "weather_temp" not in metric_map or "stock_price" not in metric_map:
        raise HTTPException(status_code=500, detail="Metrics (weather_temp, stock_price) not found in database")

    weather_temp = fetch_weather_metric()
    stock_price = fetch_stock_metric()

    metrics_to_insert = []
    if weather_temp is not None:
        metrics_to_insert.append({"device_id": device_id, "metric_id": metric_map["weather_temp"], "value": weather_temp, "timestamp": datetime.now(timezone.utc).isoformat()})
    if stock_price is not None:
        metrics_to_insert.append({"device_id": device_id, "metric_id": metric_map["stock_price"], "value": stock_price, "timestamp": datetime.now(timezone.utc).isoformat()})

    if metrics_to_insert:
        db_client.table("device_metrics").insert(metrics_to_insert).execute()
        log_info("External metrics stored successfully.")

def fetch_local_metrics(limit=10):
    """Fetches latest local device metrics."""
    response = db_client.table("device_metrics") \
        .select("value, timestamp, metrics(name)") \
        .in_("metrics.name", ["cpu_usage", "ram_usage"]) \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    return response.data or {"message": "No local metrics found"}

def fetch_weather_metrics(limit=10):
    """Fetches latest weather metrics."""
    response = db_client.table("device_metrics") \
        .select("value, timestamp, metrics(name)") \
        .eq("metrics.name", "weather_temp") \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    return response.data or {"message": "No weather metrics found"}

def fetch_stock_metrics(limit=10):
    """Fetches latest stock metrics."""
    response = db_client.table("device_metrics") \
        .select("value, timestamp, metrics(name)") \
        .eq("metrics.name", "stock_price") \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    return response.data or {"message": "No stock metrics found"}

def get_metric_id(metric_name):
    """Helper function to fetch metric ID."""
    response = db_client.table("metrics").select("id").eq("name", metric_name).execute()
    return response.data[0]["id"] if response.data else None
