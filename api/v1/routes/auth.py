"""Contains routes pertaining to authenticating a user"""
from flask import Blueprint, abort, jsonify, request
from mongoengine.errors import ValidationError
from email_validator import validate_email, EmailNotValidError

from models.user.user import User
from api.v1.routes.login import *


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.errorhandler(400)
def error_bad_request(e):
    """Raised when the parameter passed to the data is incomplete"""
    return jsonify({'error': e.description}), e.code


@auth.errorhandler(403)
def error_forbidden(e):
    """Raised when a forbidden action is attempted"""
    return jsonify({'error': e.description}), e.code


@auth.post('/create', strict_slashes=False)
def auth_create_user():
    """Creates a new user."""
    data: dict = request.get_json()

    for k in data.keys():
        if k not in ['username', 'password', 'email']:
            return abort(400, f"unprocessable entity '{k}'")

    uname = data.get('username')
    pswrd = data.get('password')
    email = data.get('email')

    if not uname:
        return abort(400, 'username not found')
    if not pswrd:
        return abort(400, 'password not found')
    if not email:
        return abort(400, 'email not found')

    try:
        valid_mail = validate_email(email)
    except EmailNotValidError:
        return abort(400, f"email address '{email}' is not valid")

    new_user = User(email=valid_mail.normalized, password=pswrd, username=uname)

    try:
        new_user.save()
    except ValidationError as e:
        # return abort(403, 'user with email \'{email}\' already exist')
        return abort(403, e.message)

    return jsonify({'username': uname, 'email': email}), 201