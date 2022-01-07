from cache.backends.base import BaseBackend
from cache.backends.base import BaseAsyncBackend
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
            raise KeyError(key)
        return self.serializer.loads(value)

    def set(self, key, value, ttl):
        value = self.serializer.dumps(value)
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        return self.client.delete(key) != 0

    def has_key(self, key):
        return self.client.exists(key) == 1

    def get_ttl(self, key):
        result = self.client.ttl(key)
        if result == -2:
            raise KeyError

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


class AsyncRedisBackend(BaseAsyncBackend):

    def __init__(self, serializer=None, client=None, **client_kwargs):
        self.serializer = serializer if serializer is None else PickleSerializer()
        if client and client_kwargs:
            raise ValueError("Cannot pass a client and client kwargs.")

        if client_kwargs:
            import aioredis
            self.client = aioredis.from_url(**client_kwargs)

        else:
            self.client = client

    async def get(self, key):
        value = await self.client.get(key)
        return MissingKey if value is None else value

    async def set(self, key, value, ttl):
        await self.client.set(key, value, ttl)

    async def delete(self, key):
        return await self.client.delete(key) > 0

    async def has_key(self, key):
        return await self.client.exists(key) == 1

    async def get_ttl(self, key):
        result = await self.client.ttl(key)
        if result == -1:
            return None

        if result == -2:
            return MissingKey

        return result

    async def set_ttl(self, key, ttl):
        if ttl is not None:
            return await self.client.expire(key, ttl)

        result = await self.client.persist(key)
        if result:
            # persist() only returns True if the wasn't already persisted.
            return result

        # If the result is False we need to check if the key exists.
        return await self.get_ttl(key) is None
