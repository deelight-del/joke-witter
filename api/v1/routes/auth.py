"""Contains routes pertaining to authenticating a user"""

import os
from datetime import datetime, timedelta, timezone

from flask import Blueprint, abort, jsonify, request, make_response
from mongoengine.errors import NotUniqueError
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import check_password_hash, generate_password_hash
from jose import jwt
from uuid import uuid4

from models.silo import Silo
from models.user.user import User


auth = Blueprint("auth", __name__, url_prefix="/auth")

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


@auth.errorhandler(400)
def error_bad_request(e):
    """Raised when the parameter passed to the data is incomplete"""
    return jsonify({"error": e.description}), e.code


@auth.errorhandler(403)
def error_forbidden(e):
    """Raised when a forbidden action is attempted"""
    return jsonify({"error": e.description}), e.code


@auth.post("/create", strict_slashes=False)
def auth_create_user():
    """Create user endpoint
    ---
    tags:
      - Auth
    parameters:
      - name: username
        in: form
        type: string
        required: true
      - name: email
        in: form
        type: string
        required: true
      - name: password
        in: form
        type: string
        required: true
    responses:
      201:
        description: A json response containing the Username and Email of the created user
        schema:
            type: object
            properties:
                username:
                    type: string
                email:
                    type: string
      400:
        description: Field not found
    """
    data: dict = request.form

    for k in data.keys():
        if k not in ["username", "password", "email"]:
            abort(400, f"unprocessable entity '{k}'")

    uname = data.get("username")
    pswrd = data.get("password")
    email = data.get("email")

    if not uname:
        abort(400, "username not found")
    if not pswrd:
        abort(400, "password not found")
    if not email:
        abort(400, "email not found")

    try:
        valid_mail = validate_email(email)
    except EmailNotValidError:
        abort(400, f"email address '{email}' is not valid")

    new_user = User(
        email=valid_mail.normalized,
        password=generate_password_hash(pswrd),
        username=uname,
    )

    try:
        new_user.save()
    except NotUniqueError as e:
        if "email" in str(e):
            abort(403, f"user with email '{email}' already exist")
        elif "username" in str(e):
            abort(403, f"user with username '{uname}' already exist")

    return jsonify({"username": uname, "email": email}), 201


@auth.post("/login", strict_slashes=False)
def login():
    """Log into a user endpoint
    ---
    tags:
      - Auth
    parameters:
      - name: username or email
        in: form
        type: string
        required: true
      - name: password
        in: form
        type: string
        required: true
    responses:
      200:
        description: A json response containing the Username and Email of the created user
        schema:
            type: object
            properties:
                username:
                    type: string
                email:
                    type: string
      400:
        description: Missing field
      401:
        description: Username or Email address not registered
    """
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
    session_id = str(uuid4())
    json_payload["session_id"] = session_id

    Silo.create_silo(session_id)
    jwt_payload = jwt.encode(json_payload, str(SECRET_KEY), algorithm="HS256")

    response = make_response({"email": user.email, "username": user.username}, 201)
    response.headers["Authorization"] = jwt_payload

    return response


# TODO: Test the session_id added to the json_payload.
