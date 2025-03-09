import psutil
from datetime import datetime

def collect_system_metrics():
    """Collects CPU and RAM usage metrics from the system."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent
    }
