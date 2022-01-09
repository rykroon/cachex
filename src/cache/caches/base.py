from cache.backends import LocalBackend
from cache.constants import DEFAULT_TTL, Default, MissingKey


class Cache:

    def __init__(
            self,
            namespace=None,
            ttl=DEFAULT_TTL,
            key_builder=None,
            backend=None
            ):
        self.namespace = namespace
        self.default_ttl = ttl
        self.key_builder = key_builder or self._default_key_builder
        self._backend = backend or LocalBackend()

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
        if ttl == 0:
            self.delete(key)

        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        self._backend.set(key, value, ttl)

    def add(self, key, value, ttl=Default):
        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        return self._backend.add(key, value, ttl)

    def delete(self, key):
        key = self.key_builder(key, self.namespace)
        return self._backend.delete(key)

    def has_key(self, key):
        key = self.key_builder(key, self.namespace)
        return self._backend.has_key(key)

    def get_many(self, *keys):
        keys = [self.key_builder(k, self.namespace) for k in keys]
        return self._backend.get_many(*keys)

    def set_many(self, mapping, ttl=Default):
        if ttl == 0:
            self.delete_many(*mapping.keys())

        new_mapping = {}
        for k, v in mapping.items():
            new_key = self.key_builder(k, self.namespace)
            new_mapping[new_key] = v

        ttl = self.default_ttl if ttl is Default else ttl
        return self._backend.set_many(new_mapping, ttl)

    def delete_many(self, *keys):
        keys = [self.key_builder(k, self.namespace) for k in keys]
        return self._backend.delete_many(*keys) 

    def get_ttl(self, key):
        key = self.key_builder(key, self.namespace)
        return self._backend.get_ttl(key)

    def set_ttl(self, key, ttl=Default):
        if ttl == 0:
            return self.delete(key)

        key = self.key_builder(key, self.namespace)
        ttl = self.default_ttl if ttl is Default else ttl
        return self._backend.set_ttl(key, ttl)

    def clear(self):
        self._backend.clear()
