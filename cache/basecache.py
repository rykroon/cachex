from cache.serializers import StringSerializer

Undefined = object()


class BaseCache:

    def __init__(self, serializer=None, namespace=None, ttl=300):
        self.serializer = serializer or StringSerializer()
        self.namespace = namespace
        self.ttl = ttl

    def __contains__(self, key):
        raise NotImplementedError

    def _build_key(self, key):
        return f'{self.namespace}{key}' if self.namespace else key

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, ttl=Undefined):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    

    