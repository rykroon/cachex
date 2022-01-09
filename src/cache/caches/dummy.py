from cache.caches.base import Cache
from cache.backends.dummy import DummyBackend
from cache.constants import DEFAULT_TTL


class DummyCache(Cache):

    def __init__(
            self,
            namespace=None,
            ttl=DEFAULT_TTL,
            key_builder=None,
    ):
        super().__init__(
            namespace=namespace,
            ttl=ttl,
            key_builder=key_builder,
            backend=DummyBackend()
        )
