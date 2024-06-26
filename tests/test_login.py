#!/usr/bin/env python3
"""Module for testing the login behaviour."""

from datetime import datetime, timedelta
import unittest
import os

from mongoengine import OperationError
from pymongo.errors import ConnectionFailure
from app import app
from models.user.user import User
from werkzeug.security import generate_password_hash
from jose import jwt
from werkzeug.exceptions import BadRequestKeyError


SECRET_KEY = os.getenv("SECRET_KEY")


class TestLogin(unittest.TestCase):
    """TestLogin Class."""

    def setUp(self) -> None:
        """Set Up Method."""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        try:
            User.drop_collection()
        except (OperationError, ConnectionFailure):
            pass
        self.user1_email = "user1@users.witter.com"
        self.user1_username = "John_Doe123"
        self.user1_password = "myverySTRONGpassword"
        self.user1_e_password = generate_password_hash(self.user1_password)
        User(
            email=self.user1_email,
            username=self.user1_username,
            password=self.user1_e_password,
        ).save()
        self.user2_email = "user2@users.witter.com"
        self.user2_username = "sheldon (coop) 89"
        self.user2_password = "12%^Unen1N9"
        self.user2_e_password = generate_password_hash(self.user2_password)
        User(
            email=self.user2_email,
            username=self.user2_username,
            password=self.user2_e_password,
        ).save()

    def tearDown(self) -> None:
        """tear Down method."""
        self.ctx.pop()
        try:
            User.drop_collection()
        except (OperationError, ConnectionFailure):
            pass

    def test_right_login(self) -> None:
        """Test the login with the right details."""
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": self.user1_email,
                "password": self.user1_password,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json, {"email": self.user1_email, "username": self.user1_username}
        )

        # Test with username.
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": self.user2_username,
                "password": self.user2_password,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json, {"email": self.user2_email, "username": self.user2_username}
        )

    def test_unexisting_details(self):
        """Test when the user email and username don't exist"""
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": "Unexisting-Username",
                "password": self.user1_password,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "email/username not registered"})
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": "Unexisting@mail.com",
                "password": self.user1_password,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "email/username not registered"})

    def test_wrong_password(self):
        """Test for when the password is wrong."""
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": self.user1_email,
                "password": self.user2_password,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"error": "email/username or password is incorrect"}
        )

    def test_missing_fields(self):
        """Test what happens when fields are missing"""
        response = self.client.post(
            "/auth/login",
            data={"password": self.user1_password},
        )
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(
        #    response.json, {"error": "Fill both username and password field"}
        # )
        response = self.client.post(
            "/auth/login",
            data={"email_or_username": self.user1_email},
        )
        self.assertEqual(response.status_code, 400)
        # self.assertEqual(
        #    response.json, {"error": "Fill both username and password field"}
        # )
        # TODO: Fix the commented out when auth.py has been fully constructed.

    def test_header_when_logged_in(self):
        """Check if the authorization header is set."""
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": self.user1_email,
                "password": self.user1_password,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json, {"email": self.user1_email, "username": self.user1_username}
        )
        self.assertIsNotNone(response.headers["Authorization"])
        auth_claims = jwt.decode(response.headers["Authorization"], key=str(SECRET_KEY))
        # The datetime claims are obtained as POSIX integer(epoch) timing.
        self.assertIsInstance(auth_claims["exp"], int)
        self.assertIsInstance(auth_claims["nbf"], int)
        self.assertGreater(auth_claims["exp"] - auth_claims["nbf"], 82800)

    def test_header_when_not_logged_in(self):
        """Check the authorization header is not set at failed login."""
        response = self.client.post(
            "/auth/login",
            data={
                "email_or_username": self.user1_username,
                "password": self.user2_password,
            },
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json, {"error": "email/username or password is incorrect"}
        )
        with self.assertRaises(BadRequestKeyError):
            response.headers["Authorization"]

    def test_wrong_http_verb(self):
        """What happens when we use the wrong http verb."""
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 405)
