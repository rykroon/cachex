import unittest

from cache.caches import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(namespace="test")

    def test_get_set(self):
        assert self.cache.get('a', default=20) == 20
        self.cache.set('a', 1)
        assert self.cache.get('a', default=20) == 1

    def test_add(self):
        assert self.cache.add('a', 1) == True
        assert self.cache.add('a', 1) == False

    def test_delete(self):
        assert self.cache.delete('a') == False
        self.cache.set('a', 1)
        assert self.cache.delete('a') == True

    def test_has_key(self):
        assert self.cache.has_key('a') == False
        self.cache.set('a', 1)
        assert self.cache.has_key('a') == True


if __name__ == '__main__':
    unittest.main()