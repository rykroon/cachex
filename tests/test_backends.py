import unittest
import time

import redis

from cache.backends.base import BaseBackend
from cache.backends.dummy import DummyBackend
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


class AbstractBackendTest:

    def test_get_missingkey(self):
        assert self.backend.get('a') is MissingKey

    def test_get_any(self):
        self.backend.set('a', 1, None)
        assert self.backend.get('a') == 1

    def test_set_persist(self):
        self.backend.set('a', 1, None)
        assert self.backend.get('a') == 1
        assert self.backend.get_ttl('a') == None
        
    def test_set_expire(self):
        self.backend.set('a', 1, 20)
        assert self.backend.get('a') == 1
        assert self.backend.get_ttl('a') == 20

    def test_delete_false(self):
        assert self.backend.delete('a') == False

    def test_delete_true(self):
        self.backend.set('a', 1, None)
        assert self.backend.delete('a') == True
        assert self.backend.get('a') is MissingKey
        
    def test_has_key_false(self):
        assert self.backend.has_key('a') == False
        self.backend.set('a', 1, 1)
        time.sleep(1)
        assert self.backend.has_key('a') == False

    def test_has_key_true(self):
        self.backend.set('a', 1, None)
        assert self.backend.has_key('a') == True

        self.backend.set('a', 1, 1)
        assert self.backend.has_key('a') == True

    def test_get_ttl(self):
        assert self.backend.get_ttl('a') is MissingKey
        
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


class TestRedisBackend(unittest.TestCase, AbstractBackendTest):
    def setUp(self):
        client = redis.Redis()
        client.flushdb()
        self.backend = RedisBackend(client=client)


class TestLocalBackend(unittest.TestCase, AbstractBackendTest):
    def setUp(self):
        self.backend = LocalBackend()


# class TestDummyBackend(unittest.TestCase, AbstractBackendTest):
#     def setUp(self):
#         self.backend = DummyBackend()


if __name__ == '__main__':
    unittest.main()