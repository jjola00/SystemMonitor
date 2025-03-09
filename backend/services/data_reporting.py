from database.db_connection import db_client
from fastapi import HTTPException

def get_recent_metrics(limit=20):
    """Fetches the latest device and third-party metrics."""
    response = db_client.table("device_metrics") \
        .select("value, timestamp, device_id, metrics(name, unit)") \
        .order("timestamp", desc=True) \
        .limit(limit) \
        .execute()

    if not response.data:
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

    return formatted_data

def get_device_name(device_id):
    """Retrieves the device name given a device ID."""
    response = db_client.table("devices").select("name").eq("id", device_id).execute()
    if response.data:
        return response.data[0]["name"]
    return "Unknown Device"
