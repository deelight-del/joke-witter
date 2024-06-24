"""Contains routes pertaining to authenticating a user"""
from flask import Blueprint, abort, jsonify, request


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.errorhandler(400)
def error_bad_request(e):
    """Raised when the parmeter passed to the data is incomplete"""
    return jsonify({'error': e.description}), e.code


@auth.errorhandler(403)
def error_forbidden(e):
    """Raised when the a forbidden action is attempted"""
    return jsonify({'error': e.description}), e.code


@auth.post('/create', strict_slashes=False)
def auth_create_user():
    """Creates a new user."""
    data: dict = request.get_json()

    uname = data.get('username')
    pswrd = data.get('password')
    email = data.get('email')

    if not uname:
        return abort(400, 'username not found')
    if not pswrd:
        return abort(400, 'password not found')
    if not email:
        return abort(400, 'email not found')

    # TODO: Check if user already exist
    user = None

    if user:
        return abort(403, 'user with email \'{email}\' already exist')

    # TODO: Store user in db

    return jsonify({'username': uname, 'email': email}), 201
