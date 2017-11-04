from flask import Flask
from flask_cors import CORS

from config import config
from . import repository


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    repository.build(app)

    from . import views
    views.register(app)

    return app
