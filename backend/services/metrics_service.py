from database.db_connection import db_client
from datetime import datetime, timezone
from collectors.system_collector import collect_system_metrics
from collectors.third_party_collector import fetch_weather_metric, fetch_crypto_metric
from utils.logger import log_info
from utils.helpers import get_local_ip
from fastapi import HTTPException


def get_or_create_device_id(device_name, ip_address=None):
    """Fetch device ID by name, or insert it if not found."""
    response = db_client.table("devices").select("id, ip_address").eq("name", device_name).execute()
    
    if response.data:
        device_id = response.data[0]["id"]
        if ip_address and response.data[0].get("ip_address") != ip_address:
            db_client.table("devices").update({"ip_address": ip_address}).eq("id", device_id).execute()
        return device_id
    
    new_device = {"name": device_name, "ip_address": ip_address, "created_at": datetime.now(timezone.utc).isoformat()}
    insert_response = db_client.table("devices").insert(new_device).execute()
    
    return insert_response.data[0]["id"] if insert_response.data else None

def store_local_metrics():
    """Fetches and stores CPU and RAM usage."""
    metrics = collect_system_metrics()
    ip_address = get_local_ip()
    device_id = get_or_create_device_id(metrics["device_name"], ip_address)

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["cpu_usage", "ram_usage"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "cpu_usage" not in metric_map or "ram_usage" not in metric_map:
        raise HTTPException(status_code=500, detail="Metrics (cpu_usage, ram_usage) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": metrics["cpu_usage"], "timestamp": datetime.now(timezone.utc).isoformat()},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": metrics["ram_usage"], "timestamp": datetime.now(timezone.utc).isoformat()}
    ]).execute()

    log_info("Local metrics stored successfully.")

def store_external_metrics():
    """Fetches and stores weather and crypto metrics."""
    device_name = "Server temp"
    device_id = get_or_create_device_id(device_name)

    # Check if metrics already exist before inserting
    existing_metrics = db_client.table("metrics").select("name").in_("name", ["weather_temp", "crypto_price"]).execute()
    existing_metric_names = {m["name"] for m in existing_metrics.data}

    metrics_to_upsert = []
    if "weather_temp" not in existing_metric_names:
        metrics_to_upsert.append({"name": "weather_temp", "unit": "°C"})
    if "crypto_price" not in existing_metric_names:
        metrics_to_upsert.append({"name": "crypto_price", "unit": "USD"})

    if metrics_to_upsert:
        db_client.table("metrics").upsert(metrics_to_upsert).execute()

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["weather_temp", "crypto_price"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    weather_temp = fetch_weather_metric()
    crypto_price = fetch_crypto_metric()

    metrics_to_insert = []
    if weather_temp is not None:
        metrics_to_insert.append({
            "device_id": device_id,
            "metric_id": metric_map["weather_temp"],
            "value": weather_temp,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    if crypto_price is not None:
        log_info(f"Crypto price: {crypto_price['value']} USD")
        metrics_to_insert.append({
            "device_id": device_id,
            "metric_id": metric_map["crypto_price"],
            "value": crypto_price["value"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

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

def fetch_crypto_metrics(limit=10):
    """Fetches latest crypto metrics."""
    response = db_client.table("device_metrics") \
        .select("value, timestamp, metrics(name)") \
        .eq("metrics.name", "crypto_price") \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    return response.data or {"message": "No crypto metrics found"}

def get_metric_id(metric_name):
    """Helper function to fetch metric ID."""
    response = db_client.table("metrics").select("id").eq("name", metric_name).execute()
    return response.data[0]["id"] if response.data else None
