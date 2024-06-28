"""Test  For Silos"""

import unittest

from models.silo import Silo
from models import REDIS


class TestSilo(unittest.TestCase):
    """Silo test case"""

    ID = "arandomid"

    def setUp(self) -> None:
        Silo.create_silo(self.ID)

    def tearDown(self) -> None:
        Silo.destroy_silo(self.ID)

    def test_redis_initialized(self):
        """Test to see if the connection to redis was successful."""
        self.assertTrue(REDIS.connected())

    def test_new_silo_created(self):
        """Test to see if a new silo was successfully created."""

        item = REDIS.get(self.ID, "jokes")
        _item = Silo.get_jokes(self.ID, 5)

        self.assertTrue(
            len(_item) == len(item[0])
        )
        self.assertLessEqual(len(_item), 5)
        self.assertListEqual(item[0], _item)

    def test_joke_id_included(self):
        """Test including a new id exists"""
        Silo.include_joke(self.ID, "0")

        self.assertTrue(REDIS.exist(self.ID, "includes", "0"))
        self.assertFalse(REDIS.exist(self.ID, "exclude", "0"))

    def test_joke_id_excluded(self):
        """Test excluding a new id exists"""
        Silo.exclude_joke(self.ID, "0")

        self.assertTrue(REDIS.exist(self.ID, "excludes", "0"))
        self.assertFalse(REDIS.exist(self.ID, "includes", "0"))

    def test_exception_if_id_destroyed(self):
        """Test if geting item after destruction id fails"""
        Silo.destroy_silo(self.ID)
        with self.assertRaises(KeyError):
            Silo.get_jokes(self.ID)

    def test_exception_if_id_not_exist(self):
        """Test if geting item with a non existent id fails"""
        with self.assertRaises(KeyError):
            Silo.get_jokes("thisiddoesnotexist")
