from flask import Flask

from nleaser_api.namespaces import api
from nleaser_sources.app_services.authentication import jwt
from nleaser_models import connect_db


def create_api():
    app = Flask(__name__)
    app.config.from_pyfile("../nleaser_config/__init__.py")
    api.init_app(app)
    jwt.init_app(app)
    connect_db()

    @app.after_request
    def enable_cors(response):
        response.headers.add("Access-Control-Allow-Headers", "authorization,content-type")
        response.headers.add("Access-Control-Allow-Methods", "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return app
