from flask import Blueprint, request

from .permission import admin_required
from .domain.errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField
from .domain.usecases import auth_view_token, auth_admin_token, \
    get_user_by_token, add_host, delete_host, list_all_host, modify_host, \
    add_service, delete_service, modify_service, get_tip
from .repos import AdminRepoImpl, HostRepoImpl, ServiceRepoImpl
from . import status

main = Blueprint('main', __name__)


@main.before_request
def parse_token():
    token = request.headers.get('token', None)
    user = get_user_by_token(AdminRepoImpl(), token)
    request.user = user


@main.route('/tip', methods=['GET'])
def tip():
    return status.respond({'tip':  get_tip(AdminRepoImpl())})


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
        return status.respond(({'token': token}))


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
def host_add():
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


@main.route('/host/<int:id>', methods=['DELETE'])
@admin_required
def host_delete(id):
    try:
        delete_host(HostRepoImpl(), id)
    except EmptyField:
        return status.respond({'msg': 'Which host do u wanna delete?'},
                              status.BAD_REQUEST)
    return status.respond(status=status.SUCCESS)


@main.route('/host', methods=['GET'])
@admin_required
def host_list_all():
    hosts = list_all_host(HostRepoImpl())
    return status.respond([host.to_json() for host in hosts])


@main.route('/host/<int:id>', methods=['PUT'])
@admin_required
def host_modify(id):
    try:
        modify_host(HostRepoImpl(), id,
                    request.json.get('name', None),
                    request.json.get('detail', None),
                    request.json.get('address', None))
    except EmptyField as e:
        if e.field == 'id':
            return status.respond({'msg': 'Which host do u wanna modify?'},
                                  status.BAD_REQUEST)
        else:
            return status.respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                status.BAD_REQUEST)
    return status.respond()


@main.route('/service', methods=['POST'])
@admin_required
def service_add():
    try:
        add_service(ServiceRepoImpl(),
                    request.json.get('host_id', None),
                    request.json.get('name', None),
                    request.json.get('detail', None),
                    request.json.get('port', None))
    except EmptyField as e:
        return status.respond(
            {'msg': 'Required field: {field}'.format(field=e.field)},
            status.BAD_REQUEST)
    return status.respond(status=status.CREATED)


@main.route('/service/<int:id>', methods=['DELETE'])
@admin_required
def service_delete(id):
    try:
        delete_service(ServiceRepoImpl(), id)
    except EmptyField:
        return status.respond({'msg': 'Which service do u wanna delete?'},
                              status.BAD_REQUEST)
    return status.respond(status=status.SUCCESS)


@main.route('/service/<int:id>', methods=['PUT'])
@admin_required
def service_modify(id):
    try:
        modify_service(ServiceRepoImpl(), id,
                       request.json.get('name', None),
                       request.json.get('detail', None),
                       request.json.get('port', None),
                       request.json.get('host_id', None))
    except EmptyField as e:
        if e.field == 'id':
            return status.respond({'msg': 'Which host do u wanna modify?'},
                                  status.BAD_REQUEST)
        else:
            return status.respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                status.BAD_REQUEST)
    return status.respond()
