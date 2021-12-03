from cache.serializers import StringSerializer
from cache.constants import DEFAULT_TTL, NotPassed, MissingKey


class Cache:

    def __init__(self, namespace=None, ttl=DEFAULT_TTL,  backend=None, serializer=None):
        self.namespace = namespace
        self.ttl = ttl
        self._backend = backend
        self._serializer = serializer or StringSerializer()

    def __contains__(self, key):
        key = self._build_key(key)
        return key in self._backend

    def _build_key(self, key):
        return f'{self.namespace}:{key}' if self.namespace else key

    def get(self, key, default=None):
        key = self._build_key(key)
        value = self._backend.get(key)
        if value is MissingKey:
            return default
        return self._serializer.loads(value)

    def set(self, key, value, ttl=NotPassed):
        key = self._build_key(key)
        value = self._serializer.dumps(value)
        ttl = self.ttl if ttl is NotPassed else ttl
        self._backend.set(key, value, ttl)

    def delete(self, key):
        key = self._build_key(key)
        self._backend.delete(key)


class AsyncCache:

    def __init__(self, namespace=None, ttl=DEFAULT_TTL,  backend=None, serializer=None):
        self.namespace = namespace
        self.ttl = ttl
        self._backend = backend
        self._serializer = serializer or StringSerializer()

    def __contains__(self, key):
        key = self._build_key(key)
        return key in self._backend

    def _build_key(self, key):
        return f'{self.namespace}:{key}' if self.namespace else key

    async def get(self, key, default=None):
        key = self._build_key(key)
        value = await self._backend.get(key)
        if value is MissingKey:
            return default
        return self._serializer.loads(value)

    async def set(self, key, value, ttl=NotPassed):
        key = self._build_key(key)
        value = self._serializer.dumps(value)
        ttl = self.ttl if ttl is NotPassed else ttl
        await self._backend.set(key, value, ttl)

    async def delete(self, key):
        key = self._build_key(key)
        await self._backend.delete(key)

