import unittest
import time

import redis
import aioredis

from cache.backends import AsyncRedisBackend, RedisBackend
from cache.constants import MissingKey


class TestRedisBackend(unittest.TestCase):

    def setUp(self):
        self.client = redis.Redis()
        self.client.flushdb()
        self.backend = RedisBackend(client=self.client)

    def test_get(self):
        assert self.backend.get('a') is MissingKey
        self.backend.set('a', b'1', None)
        assert self.backend.get('a') == b'1'

    def test_set(self):
        self.backend.set('a', b'1', None)
        assert self.backend.get('a') == b'1'
        assert self.client.ttl('a') == -1
        
        self.backend.set('a', '1', 20)
        time.sleep(1)
        assert self.client.ttl('a') == 19

    def test_delete(self):
        self.backend.set('a', b'1', None)
        self.backend.delete('a')
        assert self.backend.get('a') is MissingKey
        
    def test_contains(self):
        assert 'a' not in self.backend
        self.backend.set('a', b'1', None)
        assert 'a' in self.backend


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
        
    async def test_exists(self):
        assert await self.backend.exists('a') == False
        await self.backend.set('a', b'1', None)
        assert await self.backend.exists('a') == True

if __name__ == '__main__':
    unittest.main()