

Undefined = object()


class BaseCache:

    def __init__(self, key_prefix=None, timeout=300):
        self.key_prefix = key_prefix
        self.timeout = timeout

    def __contains__(self, key):
        raise NotImplementedError

    def _make_key(self, key):
        return f'{self.key_prefix}:{key}' if self.key_prefix else key

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, timeout=Undefined):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    

    