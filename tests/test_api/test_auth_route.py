"""Test  For Authentication routes."""

import unittest

from app import app
from api.v1.routes.auth import auth_create_user
from models.db.mongo_engine import MongoEngine


class TestAuthRoute(unittest.TestCase):
    """Auth Route testcase."""

    valid_user_data = {'username': 'auser',
                       'email': 'mail@mail.com', 'password': 'passwrd'}
    incomplete_user_data = {'username': 'auser', 'email': 'mail@mail.com'}
    invalid_user_data = {'school': 'futa', 'email': 'mail@mail.com'}

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        MongoEngine.connect("test", "ATotallyNewDB")

    def tearDown(self):
        self.ctx.pop()
        MongoEngine.disconnect('test')

    def test_user_create(self):
        """Test if a user is created successfully."""
        res = self.client.post('/auth/create', json=self.valid_user_data)
        self.assertEqual(res.status_code, 201)
        self.assertDictEqual(
            res.json,
            {
                'username': self.valid_user_data['username'],
                'email': self.valid_user_data['email']
            }
        )
        res = self.client.post('/auth/create', json=self.valid_user_data)

    def test_incorrect_content_type_sent(self):
        """Test if incorrect Content-Type returns correct error."""
        res = self.client.post('/auth/create', data='astring')
        self.assertEqual(res.status_code, 415)

    def test_missing_field_sent(self):
        """Test if a required field is missing return correct error."""
        res = self.client.post('/auth/create', json=self.incomplete_user_data)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(res.json, {'error': 'password not found'})

    def test_incorrect_field_sent(self):
        """Test if attaching a different field returns right error."""
        res = self.client.post('/auth/create', json=self.invalid_user_data)
        self.assertEqual(res.status_code, 400)
        self.assertDictEqual(
            res.json,
            {'error': 'unprocessable entity \'school\''}
        )

    def test_creating_an_already_existing_user(self):
        """Test if creating an existing user returns right error."""
