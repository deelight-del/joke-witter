"""Flask App."""

from flask import Flask
from flasgger import Swagger
from fastai.tabular.all import (
    Module,
    Embedding,
    sigmoid_range,
)

app = Flask(__name__)
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "JokeWitter",
            "version": "1.0",
        },
        "produces": [
            "application/json",
        ],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme.\nExample: "Authorization: Bearer {token}"',
            }
        },
    },
)


app.config["SWAGGER"] = {"title": "JokeWitter", "uiversion": 3}


# The class, as defined in the actual module,
class DotProduct(Module):
    """Dot Product Class that is used to construct
    the behaviour of the collab filtering
        model."""

    def __init__(self, n_users, n_items, n_factors, y_range=(-9.5, 10.5)):
        self.user_factors = Embedding(n_users, n_factors)
        self.user_bias = Embedding(n_users, 1)
        self.item_factors = Embedding(n_items, n_factors)
        self.item_bias = Embedding(n_items, 1)
        self.y_range = y_range

    def forward(self, x):
        """Define the forward propagation."""
        users = self.user_factors(x[:, 0])
        items = self.item_factors(x[:, 1])
        res = (users * items).sum(dim=1, keepdim=True)
        res += self.user_bias(x[:, 0]) + self.item_bias(x[:, 1])
        return sigmoid_range(res, *self.y_range)

from api.v1.routes.populate import main
from api.v1.routes.auth import auth

app.register_blueprint(auth)
app.register_blueprint(main)

if __name__ == "__main__":
    # TODO: Env variable to turn debug on and off
    app.run("0.0.0.0", 5000, debug=True)
