from flask import Flask
from flask_cors import CORS

from config import config
from . import repository
from . import domain


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])

    repos = repository.get(app)
    domain.inject_repos(**repos)

    from . import views
    views.register(app)

    return app
