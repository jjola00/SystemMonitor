from database.db_connection import db_client
from fastapi import HTTPException
from utils.logger import log_info, log_error

def fetch_metrics():
    log_info("Fetching metrics from the database.")
    response = db_client.table("device_metrics") \
        .select("value, timestamp, devices(name), metrics(name, unit)") \
        .order("timestamp", desc=True) \
        .limit(20) \
        .execute()

    if not response.data:
        log_info("No metrics found.")
        return []

    log_info("Metrics fetched successfully.")
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

def get_recent_metrics(limit=20):
    """Fetches the latest device and third-party metrics."""
    log_info(f"Fetching recent metrics with limit: {limit}.")
    response = db_client.table("device_metrics") \
        .select("value, timestamp, device_id, metrics(name, unit)") \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    if not response.data:
        log_error("No metrics found.")
        raise HTTPException(status_code=404, detail="No metrics found")

    formatted_data = []
    for row in response.data:
        formatted_data.append({
            "device_name": "External" if row["device_id"] is None else get_device_name(row["device_id"]),
            "metric_name": row["metrics"]["name"],
            "value": row["value"],
            "unit": row["metrics"]["unit"],
            "timestamp": row["timestamp"]
        })

    log_info("Recent metrics fetched successfully.")
    return formatted_data

def get_device_name(device_id):
    """Retrieves the device name given a device ID."""
    log_info(f"Retrieving device name for device ID: {device_id}.")
    response = db_client.table("devices").select("name").eq("id", device_id).execute()
    if response.data:
        log_info("Device name retrieved successfully.")
        return response.data[0]["name"]
    log_info("Device ID not found, returning 'Unknown Device'.")
    return "Unknown Device"