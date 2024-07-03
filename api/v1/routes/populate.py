#!/usr/bin/env python3
"""Module to populate the user jokes operations."""

from flask import Blueprint, jsonify, abort, request
import os
from jose import jwt, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError
from models.silo import Silo

main = Blueprint("main", __name__, url_prefix="/api/v1/user/main")

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


@main.before_request
def middleware():
    """Middleware for handling user authorization

    All endpoints in main will run this before their handlers.
    """
    token = request.headers.get("Authorization")

    if not token:
        abort(401, "Unauthorized")

    if not token.startswith(
        "Bearer "
    ):  # Checking if token starts with bearer i.e Bearer <token>
        abort(401, "No Bearer authorization header value found")

    try:
        payload = jwt.decode(key=SECRET_KEY, token=token.split()[-1])
        silo_session = payload.get("session_id")
        if not silo_session:
            raise JWTClaimsError

        setattr(
            request, "session_id", silo_session
        )  # sets the silo session token so it can be accessed from the routes
    except ExpiredSignatureError:
        abort(401, "Token expired")
    except JWTClaimsError:
        abort(401, "Invalid token claim")
    except JWTError:
        abort(401, "Invalid token")


@main.put("/<joke_id>/like", strict_slashes=False)
def like(joke_id: int):
    """Like joke endpoint
    ---
    tags:
      - Jokes
    security:
      - Bearer: ['Authorization']
    parameters:
      - name: joke_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Success response indicating joke liked
        schema:
            type: object
            properties:
                joke_id:
                    type: integer
      401:
        description: Unauthorized
    """
    session_id = request.session_id

    Silo.include_joke(session_id, joke_id=str(joke_id))
    return jsonify({"joke_id": joke_id})


@main.put("/<joke_id>/dislike", strict_slashes=False)
def dislike(joke_id: int):
    """Dislike joke endpoint
    ---
    tags:
      - Jokes
    parameters:
      - name: joke_id
        in: path
        type: integer
        required: true
    security:
      - Bearer: ['Authorization']
    responses:
      200:
        description: Success response indicating joke disliked
        schema:
            type: object
            properties:
                joke_id:
                    type: integer
      401:
        description: Unauthorized
    """
    session_id = request.session_id

    Silo.exclude_joke(session_id, joke_id=str(joke_id))
    return jsonify({"joke_id": joke_id})


@main.get("/populate", strict_slashes=False)
def populate():
    """Populate a users silo endpoint
    ---
    tags:
      - Jokes
    security:
      - Bearer: ['Authorization']
    responses:
      200:
        description: A json response that returns pre-generated content
        schema:
            type: object
            properties:
                content:
                    type: array
                    items:
                        type: string
      401:
        description: Unauthorized
    """
    session_id = request.session_id
    content = Silo.get_jokes(session_id)
    Silo.repopulate_jokes(
        session_id
    )  # NOTE: Can this come after we return content to user.
    return jsonify({"content": content})
