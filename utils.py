# utils.py
import time
from threading import Lock
from urllib.parse import unquote_plus

class SimpleCache:
    def __init__(self):
        self._store = {}    # key -> (expires_at, value)
        self._lock = Lock()

    def get(self, key):
        with self._lock:
            meta = self._store.get(key)
            if not meta:
                return None
            expires_at, value = meta
            if time.time() > expires_at:
                # expired -> remove and return None
                del self._store[key]
                return None
            return value

    def set(self, key, value, ttl):
        with self._lock:
            self._store[key] = (time.time() + ttl, value)

    def delete(self, key):
        with self._lock:
            self._store.pop(key, None)

    def clear(self):
        with self._lock:
            self._store.clear()

def normalize_city(city: str) -> str:
    return unquote_plus(city).strip().lower()

cache = SimpleCache()
