from database.repositories.metric_repository import MetricRepository
from utils.logger import log_info
from utils.cache import cache
from utils.cache_decorators import cached

def store_crypto_metrics(crypto_price: dict):
    metric_repo = MetricRepository()
    metric_repo.insert_crypto_metric(crypto_price)
    cache.delete("crypto_metrics")
    log_info("Crypto metrics stored successfully.")
    return {"status": "success"}

@cached(ttl_seconds=120, key_prefix="crypto_metrics")
def fetch_crypto_metrics(limit=10):
    log_info(f"Cache miss - fetching latest {limit} crypto metrics from database.")
    metric_repo = MetricRepository()
    return metric_repo.fetch_metrics(["crypto_price"], limit)