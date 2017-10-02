from flask import request

from ..repos import AdminRepoImpl
from ..domain.usecases import get_user_by_token
from .. import status
from .auth import auth
from .host import host
from .service import service


def register(app):
    @app.errorhandler(404)
    def not_found(error):
        return status.respond({'msg': 'Not found url.'}, status.NOT_FOUND)

    @app.before_request
    def parse_token():
        token = request.headers.get('token', None)
        user = get_user_by_token(AdminRepoImpl(), token)
        request.user = user

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(host, url_prefix='/host')
    app.register_blueprint(service, url_prefix='/service')
