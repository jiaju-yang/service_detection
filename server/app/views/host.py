from flask_restplus import Resource, Namespace

from app.domain.errors import EmptyField
from app.domain.usecases import add_host, delete_host, list_all_host, \
    modify_host

from . import status
from .permission import admin_required, anonymous_required
from .restful_helper import parse_argument

api = Namespace('host')


@api.route('', '/<int:id>')
class Host(Resource):
    @admin_required
    def post(self):
        args = parse_argument('name', 'detail', 'address')
        try:
            add_host(**args)
        except EmptyField as e:
            return status.respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                status.BAD_REQUEST)
        return status.respond(status=status.CREATED)

    @admin_required
    def delete(self, id):
        try:
            delete_host(id)
        except EmptyField:
            return status.respond({'msg': 'Which host do u wanna delete?'},
                                  status.BAD_REQUEST)
        return status.respond(status=status.SUCCESS)

    @anonymous_required
    def get(self):
        hosts = list_all_host()
        return status.respond([host.to_dict() for host in hosts])

    @admin_required
    def put(self, id):
        args = parse_argument('name', 'detail', 'address')
        try:
            modify_host(id, **args)
        except EmptyField as e:
            if e.field == 'id':
                return status.respond({'msg': 'Which host do u wanna modify?'},
                                      status.BAD_REQUEST)
            else:
                return status.respond(
                    {'msg': 'Required field: {field}'.format(field=e.field)},
                    status.BAD_REQUEST)
        return status.respond()
