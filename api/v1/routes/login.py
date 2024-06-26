#!/usr/bin/env python3
"""Contains endpoint for logging-in.
Should likely be appended to auth.py file.
"""

from api.v1.routes.auth import auth
from flask import request, jsonify, abort, make_response
from models.user.user import User
from werkzeug.security import check_password_hash
import os
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY: str | None = os.getenv("SECRET_KEY")
now: datetime = datetime.now(timezone.utc)
expdelta: timedelta = timedelta(hours=24)
exp: datetime = now + expdelta
json_payload: dict = {"exp": exp, "iat": now, "nbf": now}

if not SECRET_KEY:
    raise TypeError("SECRET KEY is not set in the environment!")


@auth.errorhandler(401)
def error_unauthenticated(e):
    """Error handler for error 401"""
    return jsonify({"error": e.description}), e.code


@auth.post("/login", strict_slashes=False)
def login():
    """Method for login endpoint"""
    email_or_username = request.form["email_or_username"]
    password = request.form["password"]
    if not email_or_username or not password:
        abort(400, description="Fill both username and password field")
    if "@" in str(email_or_username):
        user = User.objects(email=email_or_username).first()
        if user is None:
            abort(401, description="email/username not registered")
    else:
        user = User.objects(username=email_or_username).first()
        if user is None:
            abort(401, description="email/username not registered")
    # Now authenticate with password.
    pwhash = user.password
    if not check_password_hash(pwhash, password):
        abort(401, description="email/username or password is incorrect")
    jwt_payload = jwt.encode(json_payload, str(SECRET_KEY), algorithm="HS256")
    response = make_response({"email": user.email, "username": user.username}, 201)
    response.headers["Authorization"] = jwt_payload
    return response
