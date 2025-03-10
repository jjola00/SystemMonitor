# backend/services/crypto_service.py
from database.repositories.metric_repository import MetricRepository
from collectors.third_party_collector import fetch_crypto_metric
from utils.logger import log_info
from utils.cache import cache
from utils.cache_decorators import cached

def store_crypto_metrics():
    """Fetches and stores crypto metrics."""
    metric_repo = MetricRepository()
    crypto_price = fetch_crypto_metric()

    if crypto_price is not None:
        metric_repo.insert_crypto_metric(crypto_price)
        
        # Invalidate the cache after new data is stored
        cache.delete("crypto_metrics")
        
        log_info("Crypto metrics stored successfully.")
        return {"status": "success"}
    return {"status": "error", "message": "Failed to fetch crypto data"}

@cached(ttl_seconds=120, key_prefix="crypto_metrics")  # 2 minute cache for crypto
def fetch_crypto_metrics(limit=10):
    """Fetches latest crypto metrics with caching."""
    log_info(f"Cache miss - fetching latest {limit} crypto metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["crypto_price"], limit)