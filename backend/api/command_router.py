# backend/api/command_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.repositories.device_repository import DeviceRepository
from utils.logger import log_info

router = APIRouter()

# Define the Pydantic model for the request body
class CommandRequest(BaseModel):
    command: str

@router.post("/command/{device_name}")
def send_command_to_device(device_name: str, request: CommandRequest):
    """
    Send a command to a specific device.
    Example command: "Restart App"
    """
    command = request.command  # Extract the command from the request body
    log_info(f"Sending command '{command}' to device '{device_name}'")
    
    device_repo = DeviceRepository()
    device_id = device_repo.get_or_create_device_id(device_name)
    
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Store the command in the database
    device_repo.store_device_command(device_id, command)
    
    return {"status": "success", "message": f"Command '{command}' sent to device '{device_name}'"}

@router.get("/command/{device_name}")
def get_device_command(device_name: str):
    """
    Retrieve the latest command for a specific device.
    This endpoint is used by the device to poll for new commands.
    """
    log_info(f"Fetching latest command for device '{device_name}'")
    
    device_repo = DeviceRepository()
    device_id = device_repo.get_or_create_device_id(device_name)
    
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    
    command = device_repo.fetch_device_command(device_id)
    
    return {"status": "success", "command": command}