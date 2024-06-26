"""Flask App."""


from flask import Flask

from api.v1.routes.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True) # TODO: Env variable to turn debug on and off