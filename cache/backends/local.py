from math import ceil
import time
from cache.backends.base import BaseBackend
from cache.constants import MissingKey
from cache.serializers import PassthroughSerializer


class LocalBackend(BaseBackend):

    def __init__(self, serializer=None):
        self.serializer = serializer if serializer is not None else PassthroughSerializer()
        self.data = {}

    def _get(self, key):
        value, expires_at = self.data[key]
        
        if expires_at is not None and time.time() > expires_at:
            del self.data[key]
            raise KeyError(key)

        return value, expires_at

    def get(self, key):
        value, _ = self._get(key)
        return self.serializer.loads(value)

    def set(self, key, value, ttl):
        value = self.serializer.dumps(value)
        expires_at = None if ttl is None else time.time() + ttl
        self.data[key] = [value, expires_at]

    def delete(self, key):
        try:
            self.get(key)
            del self.data[key]
            return True

        except KeyError:
            return False

    def has_key(self, key):
        try:
            self.get(key)
            return True

        except KeyError:
            return False

    def get_ttl(self, key):
        _, expires_at = self._get(key)

        if expires_at is None:
            return None

        return ceil(expires_at - time.time())

    def set_ttl(self, key, ttl):
        if not self.has_key(key):
            return False

        expires_at = None if ttl is None else time.time() + ttl
        self.data[key][1] = expires_at
        return True
