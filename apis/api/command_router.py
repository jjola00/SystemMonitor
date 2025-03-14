from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from apis.database.db_connection import db_client
from apis.database.repositories.device_repository import DeviceRepository
from apis.utils.logger import log_info

router = APIRouter()

class CommandRequest(BaseModel):
    device_name: str
    command: str

def get_device_repo():
    return DeviceRepository(db_client)

@router.post("/command")
def send_command_to_device(request: CommandRequest, device_repo: DeviceRepository = Depends(get_device_repo)):
    command = request.command
    device_name = request.device_name
    log_info(f"Sending command '{command}' to device '{device_name}'")
    device_id = device_repo.get_or_create_device_id(device_name)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    device_repo.store_device_command(device_id, command)
    return {"status": "success", "message": f"Command '{command}' sent to device '{device_name}'"}

@router.get("/command/{device_name}")
def get_device_command(device_name: str, device_repo: DeviceRepository = Depends(get_device_repo)):
    log_info(f"Fetching next command for device '{device_name}'")
    device_id = device_repo.get_or_create_device_id(device_name)
    if not device_id:
        raise HTTPException(status_code=404, detail="Device not found")
    command = device_repo.fetch_and_clear_device_command(device_id)
    log_info(f"Fetched command: {command}")
    return {"status": "success", "command": command}
