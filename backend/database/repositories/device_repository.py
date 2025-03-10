# backend/database/repositories/device_repository.py
from database.db_connection import db_client
from datetime import datetime, timezone

class DeviceRepository:
    def get_or_create_device_id(self, device_name, ip_address=None):
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