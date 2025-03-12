from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.repositories.device_repository import DeviceRepository
from utils.logger import log_info

router = APIRouter()

class CommandRequest(BaseModel):
    command: str

@router.post("/command/{device_name}")
def send_command_to_device(device_name: str, request: CommandRequest):
    command = request.command
    log_info(f"Sending command '{command}' to device '{device_name}'")
    device_repo = DeviceRepository()
    device_id = device_repo.get_or_create_device_id(device_name)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    device_repo.store_device_command(device_id, command)
    return {"status": "success", "message": f"Command '{command}' sent to device '{device_name}'"}

@router.get("/command/{device_name}")
def get_device_command(device_name: str):
    log_info(f"Fetching latest command for device '{device_name}'")
    device_repo = DeviceRepository()
    device_id = device_repo.get_or_create_device_id(device_name)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    command = device_repo.fetch_device_command(device_id)
    return {"status": "success", "command": command}