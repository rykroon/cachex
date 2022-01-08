from cache.backends import LocalBackend
from cache.constants import DEFAULT_TTL, Default, MissingKey


class Cache:

    def __init__(
            self,
            namespace=None,
            ttl=DEFAULT_TTL,
            key_builder=None,
            backend=LocalBackend()
            ):
        self.namespace = namespace
        self.default_ttl = ttl
        self.key_builder = key_builder or self._default_key_builder
        self._backend = backend

    def __contains__(self, key):
        return self.has_key(key)

    def _default_key_builder(self, key, namespace):
        return f'{namespace}:{key}' if namespace is not None else key

    def get(self, key, default=None):
        key = self.key_builder(key, self.namespace)
        result = self._backend.get(key)
        if result is MissingKey:
            return default
        return result

    def set(self, key, value, ttl=Default):
        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        self._backend.set(key, value, ttl)

    def delete(self, key):
        key = self.key_builder(key, self.namespace)
        self._backend.delete(key)

    def has_key(self, key):
        key = self.key_builder(key, self.namespace)
        return self._backend.has_key(key)

    def get_ttl(self, key):
        key = self.key_builder(key, self.namespace)
        return self._backend.get_ttl(key)

    def set_ttl(self, key, ttl=Default):
        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        return self._backend.set_ttl(key, ttl)


class AsyncCache(Cache):

    async def get(self, key, default=None):
        key = self.key_builder(key, self.namespace)
        value = await self._backend.get(key)
        if value is MissingKey:
            return default
        return self._serializer.loads(value)

    async def set(self, key, value, ttl=Default):
        key = self.key_builder(key, self.namespace)
        value = self._serializer.dumps(value)
        ttl = self.default_ttl if ttl is Default else ttl
        await self._backend.set(key, value, ttl)

    async def delete(self, key):
        key = self.key_builder(key, self.namespace)
        await self._backend.delete(key)

    async def has_key(self, key):
        key = self.key_builder(key, self.namespace)
        return await self._backend.has_key(key)

    async def get_ttl(self, key):
        key = self.key_builder(key, self.namespace)
        return await self._backend.get_ttl(key)

    async def set_ttl(self, key, ttl=Default):
        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        return await self._backend.set_ttl(key, ttl)
