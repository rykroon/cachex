from cache.constants import MissingKey


class Backend:

    def __contains__(self, key):
        raise NotImplementedError

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


class AsyncBackend:

    async def get(self, key):
        raise NotImplementedError

    async def set(self, key, value, ttl):
        raise NotImplementedError

    async def delete(self, key):
        raise NotImplementedError


class RedisBackend(Backend):
    
    def __init__(self, client=None, **kwargs):
        if client and kwargs:
            raise ValueError

        if client:
            self.client = client

        else:
            import redis
            self.client = redis.Redis(**kwargs)

    def __contains__(self, key):
        return key in self.client

    def get(self, key):
        value = self.client.get(key)
        return MissingKey if value is None else value

    def set(self, key, value, ttl):
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        self.client.delete(key)


class AsyncRedisBackend(AsyncBackend):

    def __init__(self, client=None, **kwargs):
        if client and kwargs:
            raise ValueError

        if client:
            self.client = client

        else:
            import aioredis
            self.client = aioredis.from_url(**kwargs)
    
    async def get(self, key):
        value = await self.client.get(key)
        return MissingKey if value is None else value

    async def set(self, key, value, ttl):
        await self.client.set(key, value, ttl)

    async def delete(self, key):
        await self.client.delete(key)
