from database.db_connection import db_client

def create_tables():
    """Creates necessary tables in the database if they don't exist."""
    db_client.table("devices").upsert([
        {"id": "UUID", "name": "TEXT", "ip_address": "TEXT", "location": "TEXT", "created_at": "TIMESTAMP"}
    ]).execute()

    db_client.table("metrics").upsert([
        {"id": "UUID", "name": "TEXT", "unit": "TEXT"}
    ]).execute()

    db_client.table("device_metrics").upsert([
        {"id": "UUID", "device_id": "UUID", "metric_id": "UUID", "value": "FLOAT", "timestamp": "TIMESTAMP"}
    ]).execute()
