from functools import wraps
from utils.cache import cache

def cached(ttl_seconds=300, key_prefix=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_parts = [key_prefix, func.__name__]
            for arg in args:
                key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                key_parts.append(f"{k}={v}")
            cache_key = "_".join(key_parts)
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator