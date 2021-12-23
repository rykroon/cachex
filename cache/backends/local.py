from math import ceil
import time
from cache.backends.base import BaseBackend
from cache.constants import MissingKey


class LocalBackend(BaseBackend):

    def __init__(self):
        self.data = {}

    def __contains__(self, key):
        return self.exists(key)

    def _get(self, key):
        value, expires_at = self.data.get(key, (MissingKey, MissingKey))
        if value is not MissingKey:
            if expires_at is not None and time.time() > expires_at:
                value = MissingKey
                expires_at = MissingKey
                del self.data[key]
        return value, expires_at

    def get(self, key):
        value, _ = self._get(key)
        return value

    def set(self, key, value, ttl):
        expires_at = None if ttl is None else time.time() + ttl
        self.data[key] = (value, expires_at)

    def delete(self, key):
        try:
            del self.data[key]
        except KeyError:
            pass

    def exists(self, key):
        value = self.get(key)
        return value is not MissingKey

    def get_ttl(self, key):
        _, expires_at = self._get(key)
        if expires_at is MissingKey:
            return MissingKey
        
        if expires_at is None:
            return None
        
        return ceil(expires_at - time.time())

    def set_ttl(self, key, ttl):
        value, expires_at = self._get(key)
        if value is not MissingKey:
            expires_at = None if ttl is None else time.time() + ttl
            self.set(key, value, expires_at)
