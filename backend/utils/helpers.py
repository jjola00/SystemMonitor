from datetime import datetime

def generate_timestamp():
    """Returns the current timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def format_metric_value(value, unit):
    """Formats a metric value with its unit (e.g., 45.3% for CPU usage)."""
    return f"{value} {unit}" if unit else str(value)
