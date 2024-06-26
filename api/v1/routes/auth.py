from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/auth")

from api.v1.routes.login import *
