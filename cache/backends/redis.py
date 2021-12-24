from cache.backends.base import BaseBackend
from cache.backends.base import BaseAsyncBackend
from cache.constants import MissingKey


class RedisBackend(BaseBackend):

    @classmethod
    def create(cls, **kwargs):
        import redis
        client = redis.Redis(**kwargs)
        return cls(client=client)
    
    def __init__(self, client):
        self.client = client

    def get(self, key):
        value = self.client.get(key)
        return MissingKey if value is None else value

    def set(self, key, value, ttl):
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        return self.client.delete(key) > 0

    def has_key(self, key):
        return self.client.exists(key) == 1

    def get_ttl(self, key):
        result = self.client.ttl(key)
        if result == -1:
            return None
        
        if result == -2:
            return MissingKey

        return result

    def set_ttl(self, key, ttl):
        if ttl is not None:
            return self.client.expire(key, ttl)

        result = self.client.persist(key)
        if result:
            # persist() only returns True if the wasn't already persisted.
            return result

        # If the result is False we need to check if the key exists.
        return self.get_ttl(key) is None


class AsyncRedisBackend(BaseAsyncBackend):

    @classmethod
    def create(cls, **kwargs):
        import aioredis
        client = aioredis.from_url(**kwargs)
        return cls(client=client)

    def __init__(self, client):
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
