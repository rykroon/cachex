from typing import Any, Optional, Union
from cache.constants import UndefinedType


class BaseBackend:

    def get(self, key: str) -> Any:
        """
            Returns the value associated with the key.
            Raises KeyError if key is not found.
        """
        raise NotImplementedError

    def set(self, key: str, value: Any, ttl: Optional[int]):
        """
            Set the value of `value` to key `key`.
            The key will expire after `ttl` seconds.
            The key will never expire if `ttl` is None
        """
        raise NotImplementedError

    def add(self, key: str, value: Any, ttl: Optional[int]) -> bool:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        """
            Deletes the key
            Returns True if a key was deleted, else False
        """
        raise NotImplementedError

    def has_key(self, key: str) -> bool:
        raise NotImplementedError

    def get_many(self, keys: list[str]) -> list[Any]:
        raise NotImplementedError

    def set_many(self, mapping: dict[str, Any], ttl: Optional[int]):
        raise NotImplementedError

    def delete_many(self, keys: list[str]):
        raise NotImplementedError

    def get_ttl(self, key: str) -> Optional[int]:
        """
            Returns the TTL of the key.
            Return None if key does not have a ttl
            Raises KeyError if the key does not exist.
        """
        raise NotImplementedError

    def set_ttl(self, key: str, ttl: Optional[int]) -> bool:
        """
            Sets the TTL of the key.
            Returns True if the ttl was set, else False
        """
        raise NotImplementedError


class BaseAsyncBackend:

    async def get(self, key: str) -> Union[Any, UndefinedType]:
        raise NotImplementedError

    async def set(self, key: str, value: Any, ttl: Optional[int]):
        raise NotImplementedError

    async def delete(self, key: str) -> bool:
        raise NotImplementedError

    async def has_key(self, key: str) -> bool:
        raise NotImplementedError

    async def get_ttl(self, key: str) -> Union[int, None, UndefinedType]:
        raise NotImplementedError

    async def set_ttl(self, key: str, ttl: Optional[int]) -> bool:
        raise NotImplementedError
