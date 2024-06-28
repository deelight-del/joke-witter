"""Test  For Redis DB"""

import unittest

from models.db.redis import RedisDB, RedisError


class TestSilo(unittest.TestCase):
    """Silo test case"""

    ID = "silotest"

    def test_redis_initialized(self):
        """Test to see if the connection to redis was successful."""
        redis_db = RedisDB()
        self.assertTrue(redis_db.connected())

    def test_redis_error_invalid_host(self):
        """Test to see if a created item can be retrived"""
        redis_db = RedisDB("someinvalid host", 1000)
        self.assertFalse(redis_db.connected())

    def test_redis_error_not_intitalized(self):
        """Test to see if a created item can be retrived"""
        redis_db = RedisDB("someinvalid host", 1000)
        with self.assertRaises(RedisError):
            redis_db.set(self.ID, {})
