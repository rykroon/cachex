from typing import Any, Optional, Union
from cache.constants import UndefinedType


class BaseBackend:

    def __contains__(self, key: str):
        return self.has_key(key)

    def get(self, key: str) -> Union[Any, UndefinedType]:
        """
            Returns the value associated with the key.
            Returns Undefined if the key does not exist.
        """
        raise NotImplementedError

    def set(self, key: str , value: Any, ttl: Optional[int]):
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

    def has_key(self, key: str) -> bool:
        raise NotImplementedError

    def get_ttl(self, key: str) -> Union[int, None, UndefinedType]:
        """
            Returns the TTL of the key.
            Return None if key does not have a ttl
            Returns Undefined if the key does not exist.
        """
        raise NotImplementedError

    def set_ttl(self, key: str, ttl: Optional[int]):
        """
            Sets the TTL of the key.
        """
        raise NotImplementedError


class BaseAsyncBackend:

    async def get(self, key: str) -> Union[Any, UndefinedType]:
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl: Optional[int]):
        raise NotImplementedError

    async def delete(self, key: str):
        raise NotImplementedError

    async def has_key(self, key: str) -> bool:
        raise NotImplementedError

    async def get_ttl(self, key: str) -> Union[int, None, UndefinedType]:
        raise NotImplementedError

    async def set_ttl(self, key: str, ttl: Optional[int]):
        raise NotImplementedError