

class BaseBackend:

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


class BaseAsyncBackend:

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