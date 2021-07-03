

class BaseCache:

    def __init__(self, key_prefix=None, timeout=300):
        self.key_prefix = key_prefix
        self.timeout = timeout

    def __contains__(self, key):
        raise NotImplementedError

    def _make_key(self, key):
        if self.key_prefix:
            return '{}:{}'.format(self.key_prefix, key)
        return key

    def get(self, key, default):
        raise NotImplementedError

    def set(self, key, value, timeout=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    

    