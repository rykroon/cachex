from typing import Any, Optional, Union
from cache.constants import MissingKeyType


class BaseBackend:

    def __contains__(self, key: str):
        return self.exists(key)

    def get(self, key: str) -> Union[Any, MissingKeyType]:
        """
            Returns the value associated with the key.
            Should return MissingKey if the key does not exist
        """
        raise NotImplementedError

    def set(self, key:str , value: Any, ttl: Optional[int]):
        """
            Set the value of `value` to key `key`.
            The key will expire after `ttl` seconds.
            The key will never expire if `ttl` is None
        """
        raise NotImplementedError

    def delete(self, key: str):
        """
            Deletes the key
        """
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        raise NotImplementedError

    def get_ttl(self, key: str) -> Union[int, None, MissingKeyType]:
        """
            Returns the TTL of the key.
            Should return None if key does not have a ttl
            Or MissingKey if the key does not exist.
        """
        raise NotImplementedError

    def set_ttl(self, key: str, ttl: Optional[int]):
        """
            Sets the TTL of the key.
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

    async def get_ttl(self, key):
        raise NotImplementedError