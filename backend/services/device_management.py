from database.db_connection import db_client
from fastapi import HTTPException

def register_device(device_name, ip_address, location):
    """Registers a device in the Supabase database."""
    existing_device = db_client.table("devices").select("id").eq("name", device_name).execute()

    if existing_device.data:
        return {"message": "Device already registered", "device_id": existing_device.data[0]["id"]}

    response = db_client.table("devices").insert({
        "name": device_name,
        "ip_address": ip_address,
        "location": location
    }).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to register device")

    return {"message": "Device registered successfully", "device_id": response.data[0]["id"]}

def upload_metrics(metrics):
    """Stores device metrics (CPU & RAM usage) in Supabase."""
    device_name = metrics.get("device_name")
    cpu_usage = metrics.get("cpu_usage")
    ram_usage = metrics.get("ram_usage")

    if not device_name or cpu_usage is None or ram_usage is None:
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
        raise HTTPException(status_code=500, detail="Metrics (cpu_usage, ram_usage) not found in database")

    # Store metrics
    db_client.table("device_metrics").insert([
        {"device_id": device_id, "metric_id": metric_map["cpu_usage"], "value": cpu_usage},
        {"device_id": device_id, "metric_id": metric_map["ram_usage"], "value": ram_usage},
    ]).execute()

    return {"message": "Metrics stored successfully"}
