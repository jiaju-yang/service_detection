from flask_restplus import Resource, Namespace

from app.domain.errors import (IncorrectSign, IncorrectUsername,
                               IncorrectPassword)
from app.domain.usecases import auth_view_token, get_tip, auth_admin_token
from .response_helper import Status, respond
from .restful_helper import parse_argument

api = Namespace('auth')


@api.route('/tip')
class Tip(Resource):
    def get(self):
        return respond({'tip': get_tip()})


@api.route('/admin')
class AdminAuth(Resource):
    def post(self):
        args = parse_argument({'name': 'username', 'required': True},
                              {'name': 'password', 'required': True})
        try:
            token = auth_admin_token(**args)
        except IncorrectUsername:
            return respond({'msg': 'Incorrect username!'},
                           Status.BAD_REQUEST)
        except IncorrectPassword:
            return respond({'msg': 'Incorrect password!'},
                           Status.BAD_REQUEST)
        else:
            return respond(({'token': token}))


@api.route('/view')
class ViewAuth(Resource):
    def post(self):
        args = parse_argument({'name': 'sign', 'required': True})
        try:
            token = auth_view_token(**args)
        except IncorrectSign:
            return respond({'msg': 'Incorrect sign!'},
                           Status.BAD_REQUEST)
        else:
            return respond({'token': token})
