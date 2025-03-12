from database.db_connection import db_client
from datetime import datetime, timezone

class DeviceRepository:
    def __init__(self, db_client_instance=db_client):
        self.db_client = db_client_instance

    def get_or_create_device_id(self, device_name, ip_address=None):
        response = self.db_client.table("devices").select("id, ip_address").eq("name", device_name).execute()
        if response.data:
            device_id = response.data[0]["id"]
            if ip_address and response.data[0].get("ip_address") != ip_address:
                self.db_client.table("devices").update({"ip_address": ip_address}).eq("id", device_id).execute()
            return device_id
        new_device = {"name": device_name, "ip_address": ip_address, "created_at": datetime.now(timezone.utc).isoformat()}
        insert_response = self.db_client.table("devices").insert(new_device).execute()
        return insert_response.data[0]["id"] if insert_response.data else None
    
    def store_device_command(self, device_id: str, command: str):
        self.db_client.table("device_commands").insert({
            "device_id": device_id,
            "command": command,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }).execute()

    def fetch_and_clear_device_command(self, device_id: str):
        # Fetch the oldest unprocessed command and delete it
        response = self.db_client.table("device_commands") \
            .select("id, command") \
            .eq("device_id", device_id) \
            .order("timestamp", desc=False) \
            .limit(1) \
            .execute()
        if response.data:
            command_id = response.data[0]["id"]
            command = response.data[0]["command"]
            # Delete the command after fetching it
            self.db_client.table("device_commands") \
                .delete() \
                .eq("id", command_id) \
                .execute()
            return command
        return None