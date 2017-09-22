from flask import Blueprint, request, jsonify

from .permission import admin_required
from .domain.errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField
from .domain.usecases import auth_view_token, auth_admin_token, \
    get_user_by_token, add_host
from .repos import AdminRepoImpl, HostRepoImpl
from . import status

main = Blueprint('main', __name__)


@main.before_request
def parse_token():
    token = request.headers.get('token', None)
    user = get_user_by_token(AdminRepoImpl(), token)
    request.user = user


@main.route('/admin_auth', methods=['POST'])
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
        return jsonify({'token': token})


@main.route('/view_auth', methods=['POST'])
def view_auth():
    try:
        token = auth_view_token(AdminRepoImpl(), request.json.get('sign', None))
    except IncorrectSign:
        return status.respond({'msg': 'Incorrect sign!'}, status.BAD_REQUEST)
    else:
        return status.respond({'token': token})


@main.route('/host', methods=['POST'])
@admin_required
def host():
    try:
        add_host(HostRepoImpl(),
                 request.json.get('name', None),
                 request.json.get('detail', None),
                 request.json.get('address', None))
    except EmptyField as e:
        return status.respond(
            {'msg': 'Required field: {field}'.format(field=e.field)},
            status.BAD_REQUEST)
    return status.respond(status=status.CREATED)
