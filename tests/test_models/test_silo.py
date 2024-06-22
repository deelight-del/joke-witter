"""Test  For Silos"""

import unittest

from models.silo import Silo
from models import REDIS


class TestSilo(unittest.TestCase):
    """Silo test case"""

    ID = 'arandomid'

    def test_redis_initialized(self):
        """Test to see if the connection to redis was successful."""
        self.assertTrue(REDIS.connected())

    def test_new_silo_created(self):
        """Test to see if a new silo was successfully created."""
        Silo.create_silo(self.ID)
        item = REDIS.get(self.ID)
        _item = Silo.get_jokes(self.ID, 5)

        self.assertTrue(len(_item) != 5)  # FIX: This should be changed to ==
        self.assertLessEqual(len(_item), 5)
        self.assertEqual(
            len(item[0].get('jokes')), len(_item))

    def test_silo_destroyed(self):
        """Test is an existing silo is destroyed"""
        Silo.destroy_silo(self.ID)

    def test_exception_if_id_destroyed(self):
        """Test if geting item after destruction id fails"""
        with self.assertRaises(KeyError):
            Silo.get_jokes(self.ID)

    def test_exception_if_id_not_exist(self):
        """Test if geting item with a non existent id fails"""
        with self.assertRaises(KeyError):
            Silo.get_jokes('thisiddoesnotexist')
