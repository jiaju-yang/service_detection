from flask import Blueprint, request

from ..permission import admin_required
from ..domain.errors import EmptyField
from ..domain.usecases import add_service, modify_service, delete_service
from ..repos import ServiceRepoImpl
from .. import status


service = Blueprint('service', __name__)


@service.route('', methods=['POST'])
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


@service.route('/<int:id>', methods=['DELETE'])
@admin_required
def service_delete(id):
    try:
        delete_service(ServiceRepoImpl(), id)
    except EmptyField:
        return status.respond({'msg': 'Which service do u wanna delete?'},
                              status.BAD_REQUEST)
    return status.respond(status=status.SUCCESS)


@service.route('/<int:id>', methods=['PUT'])
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