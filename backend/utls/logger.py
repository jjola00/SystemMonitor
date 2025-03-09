import logging

# Configure logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("system_monitor.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)

def log_info(message: str):
    """Log an info message."""
    logger.info(message)

def log_warning(message: str):
    """Log a warning message."""
    logger.warning(message)

def log_error(message: str):
    """Log an error message."""
    logger.error(message)

def log_debug(message: str):
    """Log a debug message (useful for development)."""
    logger.debug(message)
