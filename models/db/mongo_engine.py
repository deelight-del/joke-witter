#!/usr/bin/env python3
"""Module for the Mongo Engine."""

from mongoengine import connect, disconnect
import os

MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT: str = os.getenv("MONGO_PORT", "27017")
DB_NAME: str = os.getenv("DB", "test")


class MongoEngine:
    """This Class will be used to create a connection with
    MongoDb and disconnect a given DB."""

    @staticmethod
    def connect(alias: str, db_name: str = DB_NAME) -> None:
        """connect method to connect to a given db and a respective alias

        Parameters
        ================
        alias - The alias to use throughout the mongo engine.

        db_name - The name of database to connect to (optional)
        Defaults to environemnt specified db_name or `test` when
        no environemnt variable is found.

        Return - None.
        """
        connect(alias=alias, host=f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{db_name}")

    @staticmethod
    def disconnect(alias: str) -> None:
        """The method to disconnect an already connected aliased database.

        Parameters
        =================
        alias - An existing aliased database.
        """
        disconnect(alias)
