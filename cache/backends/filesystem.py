import os
from cache.backends.base import BaseBackend


class FileBackend(BaseBackend):

    def __init__(self, directory):
        self.directory = directory

    def get(self, key):
        ...

    def set(self, key, value, ttl):
        ...

    def delete(self, key):
        ...

    def has_key(self, key):
        ...

    def get_ttl(self, key):
        ...

    def set_ttl(self, key, ttl):
        ...
