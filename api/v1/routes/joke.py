"""Routes for jokes functionality"""
import os
from flask import Blueprint, abort, jsonify, request
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError

from models.silo import Silo

SECRET_KEY: str | None = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise TypeError("SECRET KEY is not set in the environment!")

joke = Blueprint('joke', __name__, '/jokes')


@joke.errorhandler(401)
def error_unauthenticated(e):
    """Error handler for error 401"""
    return jsonify({"error": e.description}), e.code


@joke.errorhandler(400)
def error_bad_request(e):
    """Raised when the parameter passed to the data is incomplete"""
    return jsonify({'error': e.description}), e.code


@joke.before_request
def middleware():
    """Middleware for handling user authorization"""
    token = request.headers.get("Authorization")

    if not token:
        abort(402, 'unauthenticated')

    if not token.startswith('Bearer '):
        abort(400)

    try:
        payload = jwt.decode(key=SECRET_KEY, token=token)
        silo_session = payload.get('silo_session')
        if not silo_session:
            raise JWTClaimsError

        request.headers.set('silo_session', silo_session)
    except ExpiredSignatureError:
        abort(401, 'token expiered')
    except JWTClaimsError:
        abort(401, 'invalid token claim')
    except JWTError:
        abort(401, 'invalid token')


@joke.get('/', strict_slashes=False)
def jokes():
    """"""
    silo_session: str = request.headers['silo_session']

    jokes_avaliable = Silo.get_jokes(silo_session)
    print(jokes_avaliable)
