#!/usr/bin/env python3
"""Module to populate the user frontend.
And bulk up the silo stream."""

from flask import Blueprint, jsonify, abort, request
import os
from jose import jwt, ExpiredSignatureError, JWTError
from models.silo import Silo

main = Blueprint("main", __name__, url_prefix="/user/main")

SECRET_KEY: str | None = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise TypeError("SECRET KEY is not set in the environment!")


@main.errorhandler(401)
def error_unauthenticated(e):
    """Error handler for error 401"""
    return jsonify({"error": e.description}), e.code


@main.errorhandler(400)
def error_bad_request(e):
    """Raised when the parameter passed to the data is incomplete"""
    return jsonify({"error": e.description}), e.code


@main.errorhandler(403)
def error_forbidden(e):
    """Raised when a forbidden action is attempted"""
    return jsonify({"error": e.description}), e.code


@main.get("/populate", strict_slashes=False)
def populate():
    """Method to populate users frontend."""
    jwt_token = request.headers["Authorization"]
    if not jwt_token:
        abort(401, {"error": "Unauthorized Token"})
    try:
        json_token = jwt.decode(jwt_token, key=str(SECRET_KEY))
    except (ExpiredSignatureError, JWTError) as e:
        abort(401, {"error": str(e)})

    session_id = json_token["session_id"]
    content = Silo.get_jokes(session_id)
    Silo.repopulate_jokes(session_id)  # Can this come after sending stream to user.
    return jsonify({"content": content})
