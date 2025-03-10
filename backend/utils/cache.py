# backend/utils/cache.py
from datetime import datetime, timedelta
import threading

class Cache:
    """Simple in-memory cache with expiration"""
    
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key):
        """Get a value from cache if it exists and hasn't expired"""
        with self._lock:
            if key in self._cache:
                item = self._cache[key]
                if item['expiry'] > datetime.now():
                    return item['value']
                del self._cache[key]
        return None
    
    def set(self, key, value, ttl_seconds=300):
        """Set a value in cache with expiration time"""
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expiry': datetime.now() + timedelta(seconds=ttl_seconds)
            }
    
    def delete(self, key):
        """Remove a specific key from cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
    
    def clear(self):
        """Clear all cached items"""
        with self._lock:
            self._cache.clear()

cache = Cache()