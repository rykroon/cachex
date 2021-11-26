import pickle
import redis
from cache.basecache import BaseCache, Undefined


class RedisCache(BaseCache):

    def __init__(self, serializer=None,  namespace=None, ttl=300, *args, **kwargs):
        super().__init__(serializer, namespace, ttl)
        self.client = redis.Redis(*args, **kwargs)

    def __contains__(self, key):
        key = self._build_key(key)
        return key in self.client

    def _load(self, value):
        try:
            return pickle.loads(value)
        except pickle.UnpicklingError:
            return value

    def _dump(self, value):
        return pickle.dumps(value)
        
    def get(self, key, default=None):
        key = self._build_key(key)
        value = self.client.get(key)
        return self.serializer.loads(value) 

    def set(self, key, value, ttl=Undefined):
        key = self._build_key(key)
        value = self.serializer.dumps(value)
        ttl = self.ttl if ttl is Undefined else ttl
        return self.client.set(key, value, ex=ttl)

    def delete(self, key):
        key = self._build_key(key)
        return self.client.delete(key) == 1
