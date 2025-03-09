# backend/collectors/system_collector.py
import psutil
from datetime import datetime, timezone
from config.config import Config;

def collect_system_metrics():
    """Collects CPU and RAM usage metrics from the system."""
    return {
        "device_name": "test",
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
