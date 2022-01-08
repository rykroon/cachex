import unittest
import time

import redis

from cache.backends.local import LocalBackend
from cache.backends.redis import RedisBackend
from cache.constants import MissingKey


class TestBackend(unittest.TestCase):

    def test_all(self):
        backend = BaseBackend()
        with self.assertRaises(NotImplementedError):
            backend.get('a')

        with self.assertRaises(NotImplementedError):
            backend.set('a', b'1', None)

        with self.assertRaises(NotImplementedError):
            backend.delete('a')

        with self.assertRaises(NotImplementedError):
            backend.has_key('a')

        with self.assertRaises(NotImplementedError):
            backend.get_ttl('a')

        with self.assertRaises(NotImplementedError):
            backend.set_ttl('a', None)


class AbstractSyncBackend:

    def test_get(self):
        with self.assertRaises(KeyError):
            self.backend.get('a')

        self.backend.set('a', 1, None)
        assert self.backend.get('a') == 1

    def test_set(self):
        self.backend.set('a', 1, None)
        assert self.backend.get('a') == 1
        assert self.backend.get_ttl('a') == None
        
        self.backend.set('a', 1, 20)
        assert self.backend.get_ttl('a') == 20

    def test_delete(self):
        assert self.backend.delete('a') == False

        self.backend.set('a', 1, None)
        self.backend.delete('a')

        with self.assertRaises(KeyError):
            self.backend.get('a')
        
    def test_has_key(self):
        assert self.backend.has_key('a') == False
        self.backend.set('a', 1, None)
        assert self.backend.has_key('a') == True

        # Test that key no longer exists after expiration

    def test_get_ttl(self):
        with self.assertRaises(KeyError):
            self.backend.get_ttl('a')
        
        self.backend.set('a', 1, None)
        assert self.backend.get_ttl('a') is None
        self.backend.set('a', 1, 20)
        assert self.backend.get_ttl('a') == 20

    def test_set_ttl(self):
        # Assert setting TTL of non-existent key returns False
        assert self.backend.set_ttl('a', None) == False
        assert self.backend.set_ttl('a', 20) == False

        # Assert setting TTL of existing key returns True
        self.backend.set('a', 1, None)
        assert self.backend.set_ttl('a', None) == True
        assert self.backend.get_ttl('a') is None
        assert self.backend.set_ttl('a', 20) == True
        assert self.backend.get_ttl('a') == 20


class TestRedisBackend(unittest.TestCase, AbstractSyncBackend):
    def setUp(self):
        client = redis.Redis()
        client.flushdb()
        self.backend = RedisBackend(client=client)


class TestLocalBackend(unittest.TestCase, AbstractSyncBackend):
    def setUp(self):
        self.backend = LocalBackend()


if __name__ == '__main__':
    unittest.main()