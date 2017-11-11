from flask_restplus import Resource, Namespace

from app.domain.errors import EmptyField
from app.domain.usecases import add_service, modify_service, delete_service

from . import status
from .permission import admin_required
from .restful_helper import parse_argument

api = Namespace('service')


@api.route('', '/<int:id>')
class Service(Resource):
    @admin_required
    def post(self):
        args = parse_argument('host_id', 'name', 'detail', 'port')
        try:
            add_service(**args)
        except EmptyField as e:
            return status.respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                status.BAD_REQUEST)
        return status.respond(status=status.CREATED)

    @admin_required
    def delete(self, id):
        try:
            delete_service(id)
        except EmptyField:
            return status.respond({'msg': 'Which service do u wanna delete?'},
                                  status.BAD_REQUEST)
        return status.respond(status=status.SUCCESS)

    @admin_required
    def put(self, id):
        args = parse_argument('host_id', 'name', 'detail', 'port')
        try:
            modify_service(id, **args)
        except EmptyField as e:
            if e.field == 'id':
                return status.respond({'msg': 'Which host do u wanna modify?'},
                                      status.BAD_REQUEST)
            else:
                return status.respond(
                    {'msg': 'Required field: {field}'.format(field=e.field)},
                    status.BAD_REQUEST)
        return status.respond()
