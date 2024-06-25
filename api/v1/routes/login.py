#!/usr/bin/env python3
"""Contains endpoint for logging-in.
Should likely be appended to auth.py file.
"""

from api.v1.routes.auth import auth
from flask import request, jsonify


@auth.post("/login", strict_slashes=False)
def login():
    """Method for login endpoint"""
    email_or_username = request.form["email_or_username"]
    ...
