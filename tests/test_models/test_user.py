#!/usr/bin/env python3
"""Test User.py Module."""

import unittest
from models.user.user import User
from mongoengine import (
    OperationError,
    ConnectionFailure,
    ValidationError,
    NotUniqueError,
)
from bson.objectid import ObjectId


class TestUser(unittest.TestCase):
    """Test Class for Testing the user Class."""

    def setUp(self) -> None:
        """The setUp method."""
        try:
            User.drop_collection()
        except (OperationError, ConnectionFailure):
            pass
        self.john_email = "john@johndoe.com"
        self.john_username = "John"
        self.john_password = "mystrongpassword"
        self.mary_email = "marycoop@nail.com"
        self.mary_username = "marycooper"
        self.mary_password = "you can guess away"
        self.list_email = ["marycoop@mail.guess"]
        self.number_email = 123456
        self.list_username = ["marycoop"]
        self.number_username = 123456
        self.list_password = ["you can guess away"]
        self.number_password = 123456

    def test_multiple_users(self) -> None:
        """test multiple users."""
        john = User(
            email=self.john_email,
            username=self.john_username,
            password=self.john_password,
        )
        john.save()
        mary = User(email=self.mary_email)
        mary.username = self.mary_username
        mary.password = self.mary_password
        mary.save()
        self.assertEqual(User.objects.count(), 2)

    def test_correct_information(self) -> None:
        """Test that data is persisted with the correct info."""
        john = User(
            email=self.john_email,
            username=self.john_username,
            password=self.john_password,
        )
        john.save()
        john_from_mongo = User.objects.first()
        self.assertIsInstance(john_from_mongo, User)
        self.assertEqual(john_from_mongo.email, self.john_email)
        self.assertEqual(john_from_mongo.username, self.john_username)
        self.assertEqual(john_from_mongo.password, self.john_password)

    def test_id(self) -> None:
        """test multiple users."""
        john = User(
            email=self.john_email,
            username=self.john_username,
            password=self.john_password,
        )
        john.save()
        mary = User(email=self.mary_email)
        mary.username = self.mary_username
        mary.password = self.mary_password
        mary.save()
        john_from_mongo = User.objects(username=self.john_username).first()
        mary_from_mongo = User.objects(username=self.mary_username).first()
        self.assertIsNotNone(john_from_mongo.id)
        self.assertIsNotNone(mary_from_mongo.id)
        self.assertIsInstance(john_from_mongo.id, ObjectId)
        self.assertNotEqual(mary_from_mongo.id, john_from_mongo)
        self.assertGreater(len(str(mary_from_mongo.id)), 10)

    def test_required_fields(self) -> None:
        """test what happens when the required fields are not supplied."""
        john = User(
            username=self.john_username,
            password=self.john_password,
        )
        with self.assertRaises(ValidationError):
            john.save()
        john = User(
            email=self.john_email,
            password=self.john_password,
        )
        with self.assertRaises(ValidationError):
            john.save()
        john = User(
            username=self.john_username,
            email=self.john_email,
        )
        with self.assertRaises(ValidationError):
            john.save()
        john = User()
        with self.assertRaises(ValidationError):
            john.save()

    def test_type_check(self) -> None:
        """Using the wrong python types."""
        john = User(
            username=self.list_username,
            password=self.john_password,
            email=self.john_email,
        )
        with self.assertRaises(ValidationError):
            john.save()
        john = User(
            username=self.number_username,
            password=self.john_password,
            email=self.john_email,
        )
        with self.assertRaises(ValidationError):
            john.save()

    def test_unique_fields(self) -> None:
        """Test for email and username field to ensure uniqueness"""
        john = User(
            username=self.john_username,
            password=self.john_password,
            email=self.john_email,
        )
        john.save()
        duplicate_john_uname = User(
            username=self.john_username,
            password=self.mary_password,
            email=self.mary_email,
        )
        with self.assertRaises(NotUniqueError):
            duplicate_john_uname.save()

        mary = User(
            username=self.mary_username,
            password=self.mary_password,
            email=self.mary_email,
        )
        mary.save()
        duplicate_mary_email = User(
            username="new_mary",
            password=self.mary_password,
            email=self.mary_email,
        )
        with self.assertRaises(NotUniqueError):
            duplicate_mary_email.save()


# TODO : Test email field.
# TODO : Fix issue when mongod is not starting.
