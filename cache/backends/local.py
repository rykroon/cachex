from math import ceil
import time
from cache.backends.base import BaseBackend
from cache.constants import MissingKey
from cache.serializers import PassthroughSerializer


class LocalValue:
    def __init__(self, value, ttl):
        self.value = value
        self.set_ttl(ttl)

    def get_ttl(self):
        if self.expires_at is None:
            return None

        return max(0, ceil(self.expires_at - time.time()))

    def set_ttl(self, ttl):
        self.expires_at = None if ttl is None else time.time() + ttl

    def is_expired(self):
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at


class LocalBackend(BaseBackend):

    def __init__(self, serializer=None):
        self.serializer = serializer if serializer is not None else PassthroughSerializer()
        self.data = {}

    def _get_value(self, key):
        value = self.data.get(key)
        if value is None:
            return
        
        if value.is_expired():
            del self.data[key]
            return

        return value

    def get(self, key):
        value = self._get_value(key)
        if value is None:
            raise KeyError
        return self.serializer.loads(value.value)

    def set(self, key, value, ttl):
        value = self.serializer.dumps(value)
        self.data[key] = LocalValue(value, ttl)

    def delete(self, key):
        self._get_value(key)
        try:
            del self.data[key]
            return True

        except KeyError:
            return False

    def has_key(self, key):
        value = self._get_value(key)
        return value is not None

    def get_ttl(self, key):
        value = self._get_value(key)
        if value is not None:
            return value.get_ttl()

        raise KeyError

    def set_ttl(self, key, ttl):
        value = self._get_value(key)
        if value is None:
            return False
        value.set_ttl(ttl)
        return True
