from flask import Blueprint, request

from app import status
from app.domain.errors import (IncorrectSign, IncorrectUsername,
                               IncorrectPassword)
from app.domain.usecases import auth_view_token, get_tip, auth_admin_token

auth = Blueprint('auth', __name__)


@auth.route('/tip', methods=['GET'])
def tip():
    return status.respond({'tip': get_tip()})


@auth.route('/admin', methods=['POST'])
def admin_auth():
    try:
        token = auth_admin_token(request.json.get('username', None),
                                 request.json.get('password', None))
    except IncorrectUsername:
        return status.respond({'msg': 'Incorrect username!'},
                              status.BAD_REQUEST)
    except IncorrectPassword:
        return status.respond({'msg': 'Incorrect password!'},
                              status.BAD_REQUEST)
    else:
        return status.respond(({'token': token}))


@auth.route('/view', methods=['POST'])
def view_auth():
    try:
        token = auth_view_token(request.json.get('sign', None))
    except IncorrectSign:
        return status.respond({'msg': 'Incorrect sign!'}, status.BAD_REQUEST)
    else:
        return status.respond({'token': token})
