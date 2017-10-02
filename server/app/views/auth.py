from flask import Blueprint, request

from .. import status
from ..domain.errors import IncorrectSign, IncorrectUsername, \
    IncorrectPassword
from ..domain.usecases import auth_view_token, get_tip, auth_admin_token
from ..repos import AdminRepoImpl

auth = Blueprint('auth', __name__)


@auth.route('/tip', methods=['GET'])
def tip():
    return status.respond({'tip':  get_tip(AdminRepoImpl())})


@auth.route('/admin', methods=['POST'])
def admin_auth():
    try:
        token = auth_admin_token(AdminRepoImpl(),
                                 request.json.get('username', None),
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
        token = auth_view_token(AdminRepoImpl(), request.json.get('sign', None))
    except IncorrectSign:
        return status.respond({'msg': 'Incorrect sign!'}, status.BAD_REQUEST)
    else:
        return status.respond({'token': token})