# backend/collectors/system_collector.py
import psutil
from datetime import datetime, timezone
from utils.logger import log_info, log_error  

def collect_system_metrics():
    log_info("Collecting system metrics...") 
    try:
        metrics = {
            "device_name": "test",
            "cpu_usage": psutil.cpu_percent(interval=1),
            "ram_usage": psutil.virtual_memory().percent,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        log_info("System metrics collected successfully.") 
        return metrics
    except Exception as e:
        log_error(f"Error collecting system metrics: {e}") 
        return None
