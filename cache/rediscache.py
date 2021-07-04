import pickle
import redis
from .basecache import BaseCache


class RedisCache(BaseCache):

    def __init__(self, key_prefix=None, timeout=300, *args, **kwargs):
        super().__init__(key_prefix, timeout)
        self.client = redis.Redis(*args, **kwargs)

    def __contains__(self, key):
        key = self._make_key(key)
        return key in self.client

    def _load(self, value):
        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            return value

    def _dump(self, value):
        return pickle.dumps(value)
        
    def get(self, key, default=None):
        key = self._make_key(key)
        value = self.client.get(key)
        if value is None:
            return default
        
        return self._load(value)

    def set(self, key, value, timeout=None):
        key = self._make_key(key)
        value = self._dump(value)
        timeout = self.timeout if timeout is None else timeout
        return self.client.set(key, value, ex=timeout)

    def delete(self, key):
        key = self._make_key(key)
        return self.client.delete(key) == 1
