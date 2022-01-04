import errno
import os
from cache.backends.base import BaseBackend


"""
    Ideas...
    With the addition of a filesystem cache a new issue emerges which might require a design 
    change. 
        I am thinking that a serializer should have a dump() and a load() method (in addition
    to the already existsing loads() and dumps() methods.) These new methods will be responsible
    for serializing and deserializing the data to and from files. This makes sense because the
    json and pickle libraries already contain their own load() and dump() methods. 
        Additionally, the Serializers should be instantiated within a Backend. So instead of 
    a Cache instance having both a serializer and a backend, it will just have a backend, and
    then the backend will have it's own serializer. This is probably a better design because not
    all serializers are compatible with all backends, so a backend should be able to check which
    serializers are compatible with itself.
"""


class FileBackend(BaseBackend):

    def __init__(self, directory):
        self.directory = directory

        try:
            os.makedirs(self._path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise

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
