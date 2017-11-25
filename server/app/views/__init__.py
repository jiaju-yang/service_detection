from flask import request
from flask_restplus import Api

from app.domain.errors import NoAdministratorFound, SDException
from app.domain.usecases import get_user_by_token
from . import restful_helper, host, auth, service
from .response_helper import Status, respond


def register(app):
    @app.errorhandler(404)
    def not_found(error):
        return respond({'msg': 'Url not found.'}, Status.NOT_FOUND)

    @app.errorhandler(SDException)
    def handle_error(e):
        if isinstance(e, NoAdministratorFound):
            return respond({'msg': 'Please create an administrator first.'},
                           Status.INTERNAL_SERVER_ERROR)
        else:
            return respond({'msg': 'Unknown error just happened.'},
                           Status.INTERNAL_SERVER_ERROR)

    @app.before_request
    def parse_token():
        token = request.headers.get('token', None)
        user = get_user_by_token(token)
        request.user = user

    api = Api()
    api.add_namespace(auth.api)
    api.add_namespace(host.api)
    api.add_namespace(service.api)
    api.init_app(app)
