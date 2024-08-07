#!/usr/bin/env python3
"""Test the endpoint of the populate endpoint"""

import unittest
import random

from jose import jwt
from app import app
from mongoengine import OperationError
from pymongo.errors import ConnectionFailure
from models.user.user import User
from werkzeug.security import generate_password_hash
import os

from models.silo import Silo
from models import REDIS

SECRET_KEY: str | None = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise TypeError("SECRET KEY is not set in the environment!")


class TestPopulate(unittest.TestCase):
    """Class that inheirts from TestCase"""

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
        response = self.client.post(
            "/api/v1/auth/login",
            data={
                "email_or_username": self.user1_email,
                "password": self.user1_password,
            },
        )
        self.jwt_string = response.headers["Authorization"]
        json_payload = jwt.decode(self.jwt_string.split()[-1], str(SECRET_KEY))
        self.session_id = json_payload["session_id"]
        Silo.create_silo(self.session_id)
        Silo.include_joke(self.session_id, "2")
        Silo.include_joke(self.session_id, "20")
        self.include_random = random.randint(5, 10)
        self.exclude_random = random.randint(5, 10)

    def tearDown(self) -> None:
        """tear Down method."""
        self.ctx.pop()
        try:
            User.drop_collection()
        except (OperationError, ConnectionFailure):
            pass
        Silo.destroy_silo(self.session_id)

    def test_populate_behaviour(self) -> None:
        """Test the login with the right details."""
        resp = self.client.get(
            "/api/v1/user/main/populate",
            headers={"Authorization": self.jwt_string},
        )
        self.assertIsInstance(resp.json, dict)
        resp = self.client.get(
            "/api/v1/user/main/populate",
            headers={"Authorization": self.jwt_string},
        )
        self.assertIsInstance(resp.json, dict)
        resp = self.client.get(
            "/api/v1/user/main/populate",
            headers={"Authorization": self.jwt_string},
        )
        self.assertIsInstance(resp.json, dict)

    def test_like_behaviour(self) -> None:
        """Test liking a joke works"""
        resp = self.client.put(
            f"/api/v1/user/main/{self.include_random}/like",
            headers={"Authorization": self.jwt_string},
        )

        self.assertEqual(resp.status_code, 200)
        likes = list(
            map(int, REDIS.get(self.session_id, "includes")[0].keys()))
        self.assertIn(self.include_random, likes)

    def test_dislike_behaviour(self) -> None:
        """Test disliking a joke works"""
        resp = self.client.put(
            f"/api/v1/user/main/{self.exclude_random}/dislike",
            headers={"Authorization": self.jwt_string},
        )

        self.assertEqual(resp.status_code, 200)
        dislikes = list(
            map(int, REDIS.get(self.session_id, "excludes")[0].keys()))
        self.assertIn(self.exclude_random, dislikes)
