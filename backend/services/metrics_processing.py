from datetime import datetime
from database.db_connection import db_client
from collectors.third_party_collector import fetch_weather_metric, fetch_stock_metric

def store_external_metrics():
    """Fetches and stores third-party metrics (weather and stock price)."""
    weather_value = fetch_weather_metric()
    stock_value = fetch_stock_metric()

    metric_ids = db_client.table("metrics").select("id, name").in_("name", ["weather_temp", "stock_price"]).execute()
    metric_map = {m["name"]: m["id"] for m in metric_ids.data}

    if "weather_temp" not in metric_map or "stock_price" not in metric_map:
        raise ValueError("Metrics (weather_temp, stock_price) not found in database")

    db_client.table("device_metrics").insert([
        {"device_id": None, "metric_id": metric_map["weather_temp"], "value": weather_value, "timestamp": datetime.utcnow()},
        {"device_id": None, "metric_id": metric_map["stock_price"], "value": stock_value, "timestamp": datetime.utcnow()},
    ]).execute()

    return {"weather_temp": weather_value, "stock_price": stock_value}
