from database.db_connection import db_client
from fastapi import HTTPException
from collectors.third_party_collector import fetch_weather_metric, fetch_stock_metric
from datetime import datetime
from utils.logger import log_info, log_error

def register_device(device_name, ip_address, location):
    """Registers a device in the Supabase database."""
    existing_device = db_client.table("devices").select("id").eq("name", device_name).execute()

    if existing_device.data:
        log_info(f"Device already registered: {device_name}")
        return {"message": "Device already registered", "device_id": existing_device.data[0]["id"]}

    response = db_client.table("devices").insert({
        "name": device_name,
        "ip_address": ip_address,
        "location": location
    }).execute()

    if not response.data:
        log_error("Failed to register device.")
        raise HTTPException(status_code=500, detail="Failed to register device")

    log_info(f"Device registered successfully: {device_name}")
    return {"message": "Device registered successfully", "device_id": response.data[0]["id"]}

def upload_metrics(metrics):
    """Stores device metrics (CPU & RAM usage) in Supabase."""
    device_name = metrics.get("device_name")
    cpu_usage = metrics.get("cpu_usage")
    ram_usage = metrics.get("ram_usage")

    if not device_name or cpu_usage is None or ram_usage is None:
        log_error("Missing required fields in metrics.")
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Get or register device
    device_response = db_client.table("devices").select("id").eq("name", device_name).execute()
    if device_response.data:
        device_id = device_response.data[0]["id"]
    else:
        device_insert = db_client.table("devices").insert({"name": device_name}).execute()
        device_id = device_insert.data[0]["id"]

    # Get metric IDs for CPU & RAM
    metric_response = db_client.table("metrics").select("id, name").in_("name", ["cpu_usage", "ram_usage"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_response.data}

    if "cpu_usage" not in metric_map or "ram_usage" not in metric_map:
        log_error("Metrics not found in database.")
        raise HTTPException(status_code=500, detail="Metrics (cpu_usage, ram_usage) not found in database")

    # Store metrics
    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": cpu_usage},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": ram_usage},
    ]).execute()

    log_info("Metrics stored successfully.")
    return {"message": "Metrics stored successfully"}

def store_metrics(metrics: dict):
    device_name = metrics.get("device_name")
    cpu_usage = metrics.get("cpu_usage")
    ram_usage = metrics.get("ram_usage")

    if not device_name or cpu_usage is None or ram_usage is None:
        log_error("Missing required fields in metrics.")
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
        log_error("Metrics not found in database.")
        raise ValueError("Metrics (cpu_usage, ram_usage) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": cpu_usage, "timestamp": datetime.utcnow()},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": ram_usage, "timestamp": datetime.utcnow()},
    ]).execute()

def store_external_metrics():
    """Fetches and stores third-party metrics (weather and stock price)."""
    weather_value = fetch_weather_metric()
    stock_value = fetch_stock_metric()

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["weather_temp", "stock_price"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "weather_temp" not in metric_map or "stock_price" not in metric_map:
        log_error("Metrics not found in database.")
        raise ValueError("Metrics (weather_temp, stock_price) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": None, "metric_id": metric_map["weather_temp"], "value": weather_value, "timestamp": datetime.utcnow()},
        {"device_id": None, "metric_id": metric_map["stock_price"], "value": stock_value, "timestamp": datetime.utcnow()},
    ]).execute()

    log_info("External metrics stored successfully.")
    return {"weather_temp": weather_value, "stock_price": stock_value}
