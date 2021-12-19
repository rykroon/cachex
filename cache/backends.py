from cache.constants import MissingKey


class Backend:

    def __contains__(self, key):
        return self.exists(key)

    def get(self, key):
        """
            Returns the value associated with the key.
            Should return MissingKey if the key does not exist
        """
        raise NotImplementedError

    def set(self, key, value, ttl):
        """
            Set the value of `value` to key `key`.
            The key will expire after `ttl` seconds.
            The key will never expire if `ttl` is None
        """
        raise NotImplementedError

    def delete(self, key):
        """
            Deletes the key
        """
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def ttl(self, key):
        """
            Returns the TTL of the key.
            Should return None if key does not have a ttl
            Or MissingKey if the key does not exist.
        """
        raise NotImplementedError


class AsyncBackend:

    async def get(self, key):
        raise NotImplementedError

    async def set(self, key, value, ttl):
        raise NotImplementedError

    async def delete(self, key):
        raise NotImplementedError

    async def exists(self, key):
        raise NotImplementedError

    async def ttl(self, key):
        raise NotImplementedError


class RedisBackend(Backend):

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

    def exists(self, key):
        return self.client.exists(key) == 1

    def ttl(self, key):
        result = self.client.ttl(key)
        if result == -1:
            return None
        
        if result == -2:
            return MissingKey

        return result


class AsyncRedisBackend(AsyncBackend):

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

    async def exists(self, key):
        return await self.client.exists(key) == 1

    async def ttl(self, key):
        result = await self.client.ttl(key)
        if result == -1:
            return None
        
        if result == -2:
            return MissingKey

        return result
