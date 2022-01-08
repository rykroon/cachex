from cache.backends.base import BaseBackend
from cache.constants import MissingKey
from cache.serializers import PickleSerializer


class RedisBackend(BaseBackend):

    def __init__(self, serializer=None, client=None, **client_kwargs):
        self.serializer = serializer if serializer is not None else PickleSerializer()
        if client and client_kwargs:
            raise ValueError("Cannot pass a client and client kwargs.")

        if client:
            self.client = client
            return

        import redis
        self.client = redis.Redis(**client_kwargs)

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            return MissingKey
        return self.serializer.loads(value)

    def set(self, key, value, ttl):
        value = self.serializer.dumps(value)
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        return self.client.delete(key) != 0

    def has_key(self, key):
        return self.client.exists(key) == 1

    def get_many(self, *keys):
        values = self.client.mget(*keys)
        values = (MissingKey if v is None else self.serializer.loads(v) for v in values)
        return {k: v for k, v in zip(keys, values) if v is not MissingKey}

    def set_many(self, mapping, ttl):
        mapping = {k: self.serializer.dumps(v) for k, v in mapping.items()}
        self.client.mset(mapping)
        # need to add logic to set ttl

    def delete_many(self, *keys):
        self.client.delete(*keys)

    def get_ttl(self, key):
        result = self.client.ttl(key)
        if result == -2:
            return MissingKey

        if result == -1:
            return None

        return result

    def set_ttl(self, key, ttl):
        if ttl is not None:
            return self.client.expire(key, ttl)

        result = self.client.persist(key)
        if result:
            # persist() only returns True if the key wasn't already persisted.
            return result

        # If the result is False we need to check if the key exists.
        return self.has_key(key)
