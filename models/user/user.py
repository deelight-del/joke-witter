#!/usr/bin/env python3
"""Using Mongo Engine to define a user Object."""

from mongoengine import Document, IntField, ListField, StringField, EmailField
from models.db.mongo_engine import MongoEngine
import os

alias: str = os.getenv("DB_ALIAS", "test_witter")
MongoEngine.connect(alias)


class User(Document):
    """The user class that will be used to
    contain the information
    of each User document stored on the mongoengine"""

    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    include_ids = ListField(IntField)
    exclude_ids = ListField(IntField)
    # TODO: Test both include_ids & exclude_ids field.
    meta = {"db_alias": alias, "collection": "user"}
