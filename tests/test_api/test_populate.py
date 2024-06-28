#!/usr/bin/env python3
"""Test the endpoint of the populate endpoint"""

import unittest

from jose import jwt
from app import app
from mongoengine import OperationError
from pymongo.errors import ConnectionFailure
from models.user.user import User
from werkzeug.security import generate_password_hash
import os

from models.silo import Silo

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
            "/auth/login",
            data={
                "email_or_username": self.user1_email,
                "password": self.user1_password,
            },
        )
        self.jwt_string = response.headers["Authorization"]
        json_payload = jwt.decode(self.jwt_string, str(SECRET_KEY))
        self.session_id = json_payload["session_id"]
        Silo.create_silo(self.session_id)
        Silo.include_joke(self.session_id, "2")
        Silo.include_joke(self.session_id, "20")

    def tearDown(self) -> None:
        """tear Down method."""
        self.ctx.pop()
        try:
            User.drop_collection()
        except (OperationError, ConnectionFailure):
            pass
        Silo.destroy_silo(self.session_id)

    def test_right_behaviour(self) -> None:
        """Test the login with the right details."""
        resp = self.client.get(
            "/user/main/populate", headers={"Authorization": f"Bearer {self.jwt_string}"}
        )
        print("\n\n1. This is the resp.json\n\n", resp.json)
        self.assertIsInstance(resp.json, dict)
        resp = self.client.get(
            "/user/main/populate", headers={"Authorization": f"Bearer {self.jwt_string}"}
        )
        print("\n\n2. This is the resp.json", resp.json)
        self.assertIsInstance(resp.json, dict)
        resp = self.client.get(
            "/user/main/populate", headers={"Authorization": f"Bearer {self.jwt_string}"}
        )
        print("\n\n3. This is the resp.json", resp.json)
        self.assertIsInstance(resp.json, dict)
