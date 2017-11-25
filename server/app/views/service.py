from flask_restplus import Resource, Namespace

from app.domain.errors import EmptyField
from app.domain.usecases import add_service, modify_service, delete_service
from .permission import admin_required
from .response_helper import Status, respond
from .restful_helper import parse_argument

api = Namespace('service')


@api.route('', '/<id>')
class Service(Resource):
    @admin_required
    def post(self):
        args = parse_argument('host_id', 'name', 'detail', 'port')
        try:
            add_service(**args)
        except EmptyField as e:
            return respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                Status.BAD_REQUEST)
        return respond(status=Status.CREATED)

    @admin_required
    def delete(self, id):
        try:
            delete_service(id)
        except EmptyField:
            return respond({'msg': 'Which service do u wanna delete?'},
                           Status.BAD_REQUEST)
        return respond()

    @admin_required
    def put(self, id):
        args = parse_argument('host_id', 'name', 'detail', 'port')
        try:
            modify_service(id, **args)
        except EmptyField as e:
            if e.field == 'id':
                return respond({'msg': 'Which host do u wanna modify?'},
                               Status.BAD_REQUEST)
            else:
                return respond(
                    {'msg': 'Required field: {field}'.format(field=e.field)},
                    Status.BAD_REQUEST)
        return respond()
