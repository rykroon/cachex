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
        self.client.delete(key)

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
        if ttl is None:
            self.client.persist(key)
        else:
            self.client.expire(key, ttl)


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
        await self.client.delete(key)

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
        if ttl is None:
            self.client.persist(key)
        else:
            self.client.expire(key, ttl)
