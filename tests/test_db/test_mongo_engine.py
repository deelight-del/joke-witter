#!/usr/bin/env python3
"""Testing module for testing the Mongo Engine."""

import unittest

from mongoengine.connection import mongoengine
from models.db.mongo_engine import MongoEngine
from mongoengine import ConnectionFailure


class TestMongoEngine(unittest.TestCase):
    """The test class for testing the MongoEngine."""

    def test_connect(self) -> None:
        """This will contain the test suite for the connect.
        method.
        """
        MongoEngine.connect("test", "dbName1")
        self.assertIsNotNone(mongoengine.get_connection("test"))

        # Connect to a new Db with same alias.
        with self.assertRaises(ConnectionFailure):
            MongoEngine.connect("test", "ATotallyNewDB")

    def test_disconnect(self) -> None:
        """Method to test for the disconnect of the MongoEngine"""
        # disconnect before connecting to a new db.
        MongoEngine.connect("test", "dbName1")
        MongoEngine.disconnect("test")

        # Try to obtain get_connection after disconnecting alias.
        with self.assertRaises(ConnectionFailure):
            self.assertIsNone(mongoengine.get_connection("test"))
        # Connect to a new database after disconnect.
        MongoEngine.connect("test", "ATotallyNewDB")
        self.assertIsNotNone(mongoengine.get_connection("test"))

    def tearDown(self) -> None:
        """The tear down method."""
        mongoengine.disconnect("test")
