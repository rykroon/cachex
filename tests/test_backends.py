import unittest
import time

import redis
import aioredis

from cache.backends.base import BaseBackend, BaseAsyncBackend
from cache.backends.local import LocalBackend
from cache.backends.redis import AsyncRedisBackend, RedisBackend
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


class TestAsyncBackend(unittest.IsolatedAsyncioTestCase):

    async def test_all(self):
        backend = BaseAsyncBackend()
        with self.assertRaises(NotImplementedError):
            await backend.get('a')

        with self.assertRaises(NotImplementedError):
            await backend.set('a', b'1', None)

        with self.assertRaises(NotImplementedError):
            await backend.delete('a')


class AbstractSyncBackend:

    def test_get(self):
        assert self.backend.get('a') is MissingKey
        self.backend.set('a', b'1', None)
        assert self.backend.get('a') == b'1'

    def test_set(self):
        self.backend.set('a', b'1', None)
        assert self.backend.get('a') == b'1'
        assert self.backend.get_ttl('a') == None
        
        self.backend.set('a', '1', 20)
        assert self.backend.get_ttl('a') == 20

    def test_delete(self):
        self.backend.set('a', b'1', None)
        self.backend.delete('a')
        assert self.backend.get('a') is MissingKey
        
    def test_has_key(self):
        assert self.backend.has_key('a') == False
        self.backend.set('a', b'1', None)
        assert self.backend.has_key('a') == True

    def test_get_ttl(self):
        assert self.backend.get_ttl('a') is MissingKey
        self.backend.set('a', b'1', None)
        assert self.backend.get_ttl('a') is None
        self.backend.set('a', b'1', 20)
        assert self.backend.get_ttl('a') == 20

    def test_set_ttl(self):
        ...


class TestRedisBackend(unittest.TestCase, AbstractSyncBackend):
    def setUp(self):
        client = redis.Redis()
        client.flushdb()
        self.backend = RedisBackend(client=client)


class TestLocalBackend(unittest.TestCase, AbstractSyncBackend):
    def setUp(self):
        self.backend = LocalBackend()


class TestAsyncRedisBackend(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.client = aioredis.from_url('redis://localhost')
        await self.client.flushdb()
        self.backend = AsyncRedisBackend(client=self.client)

    async def test_get(self):
        assert await self.backend.get('a') is MissingKey
        await self.backend.set('a', b'1', None)
        assert await self.backend.get('a') == b'1'

    async def test_set(self):
        await self.backend.set('a', b'1', None)
        assert await self.backend.get('a') == b'1'
        assert await self.client.ttl('a') == -1
        
        await self.backend.set('a', '1', 20)
        time.sleep(1)
        assert await self.client.ttl('a') == 19

    async def test_delete(self):
        await self.backend.set('a', b'1', None)
        await self.backend.delete('a')
        assert await self.backend.get('a') is MissingKey
        
    async def test_has_key(self):
        assert await self.backend.has_key('a') == False
        await self.backend.set('a', b'1', None)
        assert await self.backend.has_key('a') == True

    async def test_ttl(self):
        assert await self.backend.get_ttl('a') is MissingKey
        await self.backend.set('a', b'1', None)
        assert await self.backend.get_ttl('a') is None
        await self.backend.set('a', b'1', 20)
        assert await self.backend.get_ttl('a') == 20


if __name__ == '__main__':
    unittest.main()