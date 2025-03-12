from datetime import datetime, timedelta
import threading

class Cache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key):
        with self._lock:
            if key in self._cache:
                item = self._cache[key]
                if item['expiry'] > datetime.now():
                    return item['value']
                del self._cache[key]
        return None
    
    def set(self, key, value, ttl_seconds=300):
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expiry': datetime.now() + timedelta(seconds=ttl_seconds)
            }
    
    def delete(self, key):
        with self._lock:
            if key in self._cache:
                del self._cache[key]
cache = Cache()