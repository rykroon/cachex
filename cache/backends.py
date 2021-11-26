


class Backend:

    def get(self, key, default=None):
        """
            Returns the value associated with the key.
            Returns default if the key does not exist.
        """
        raise NotImplementedError

    def set(self, key, value, ttl=None):
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


class RedisBackend(Backend):
    ...

