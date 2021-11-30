from cache.serializers import StringSerializer
from cache.sentinels import Undefined


class Cache:

    def __init__(self, namespace=None, ttl=300,  backend=None, serializer=None):
        self.namespace = namespace
        self.ttl = ttl
        self._backend = backend
        self._serializer = serializer or StringSerializer()

    def __contains__(self, key):
        return key in self._backend

    def _build_key(self, key):
        return f'{self.namespace}{key}' if self.namespace else key

    def get(self, key, default=None):
        key = self._build_key(key)
        value = self._backend.get(key)
        value = self._serializer.loads(value)
        return value if value is not None else default

    def set(self, key, value, ttl=Undefined):
        key = self._build_key(key)
        value = self._serializer.dumps(value)
        ttl = self.ttl if ttl is Undefined else ttl
        self._backend.set(key, value, ttl)

    def delete(self, key):
        key = self._build_key(key)
        self._backend.delete(key)

