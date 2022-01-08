from cache.backends.base import BaseBackend
from cache.constants import MissingKey


class DummyBackend(BaseBackend):

    def get(self, key):
        return MissingKey

    def set(self, key, value, ttl):
        pass

    def add(self, key, value, ttl):
        return False

    def delete(self, key):
        return False

    def has_key(self, key):
        return False

    def get_ttl(self, key):
        return MissingKey

    def set_ttl(self, key, ttl):
        return False
