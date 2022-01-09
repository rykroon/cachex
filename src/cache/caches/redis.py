from cache.caches.base import Cache
from cache.backends.redis import RedisBackend
from cache.constants import DEFAULT_TTL


class RedisCache(Cache):

    def __init__(
            self,
            namespace=None,
            ttl=DEFAULT_TTL,
            key_builder=None,
            **kwargs
    ):
        super().__init__(
            namespace=namespace, 
            ttl=ttl, 
            key_builder=key_builder, 
            backend=RedisBackend(**kwargs)
        )
