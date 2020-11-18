from flask import Flask

from api import api
from sources.authentication import jwt
from models import connect_db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("setup.py")
    api.init_app(app)
    jwt.init_app(app)
    connect_db()
    return app
