from flask import Blueprint, request

from ..permission import admin_required, anonymous_required
from ..domain.errors import EmptyField
from ..domain.usecases import add_host, delete_host, list_all_host, modify_host
from ..repos import HostRepoImpl
from .. import status


host = Blueprint('host', __name__)


@host.route('/', methods=['POST'])
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


@host.route('/<int:id>', methods=['DELETE'])
@admin_required
def host_delete(id):
    try:
        delete_host(HostRepoImpl(), id)
    except EmptyField:
        return status.respond({'msg': 'Which host do u wanna delete?'},
                              status.BAD_REQUEST)
    return status.respond(status=status.SUCCESS)


@host.route('/', methods=['GET'])
@anonymous_required
def host_list_all():
    hosts = list_all_host(HostRepoImpl())
    return status.respond([host.to_json() for host in hosts])


@host.route('/<int:id>', methods=['PUT'])
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
