# backend/services/crypto_service.py
from database.repositories.metric_repository import MetricRepository
from collectors.third_party_collector import fetch_crypto_metric
from utils.logger import log_info

def store_crypto_metrics():
    """Fetches and stores crypto metrics."""
    metric_repo = MetricRepository()
    crypto_price = fetch_crypto_metric()

    if crypto_price is not None:
        metric_repo.insert_crypto_metric(crypto_price)
        log_info("Crypto metrics stored successfully.")

def fetch_crypto_metrics(limit=10):
    """Fetches latest crypto metrics."""
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["crypto_price"], limit)