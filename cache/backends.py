from cache.sentinels import NoTTL, Missing


class Backend:

    def __contains__(self, key):
        raise NotImplementedError

    def get(self, key):
        """
            Returns the value associated with the key.
            Should return Undefined if the key does not exist
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
    
    def __init__(self, client):
        self.client = client

    def __contains__(self, key):
        return key in self.client

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, ttl):
        self.client.set(key, value, ex=ttl)

    def delete(self, key):
        self.client.delete(key)

