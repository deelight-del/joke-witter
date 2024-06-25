#!/usr/bin/env python3
"""Using Mongo Engine to define a user Object."""

from mongoengine import Document, StringField
from models.db.mongo_engine import MongoEngine
import os

alias: str = os.getenv("DB_ALIAS", "test_witter")
MongoEngine.connect(alias)


class User(Document):
    """The user class that will be used to
    contain the information
    of each User document stored on the mongoengine"""

    email = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
    meta = {"db_alias": alias, "collection": "user"}