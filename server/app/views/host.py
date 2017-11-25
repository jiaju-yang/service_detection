from flask_restplus import Resource, Namespace

from app.domain.errors import EmptyField
from app.domain.usecases import add_host, delete_host, list_all_host, \
    modify_host
from .permission import admin_required, anonymous_required
from .response_helper import Status, respond
from .restful_helper import parse_argument

api = Namespace('host')


@api.route('', '/<id>')
class Host(Resource):
    @admin_required
    def post(self):
        args = parse_argument('name', 'detail', 'address')
        try:
            add_host(**args)
        except EmptyField as e:
            return respond(
                {'msg': 'Required field: {field}'.format(field=e.field)},
                Status.BAD_REQUEST)
        return respond(status=Status.CREATED)

    @admin_required
    def delete(self, id):
        try:
            delete_host(id)
        except EmptyField:
            return respond({'msg': 'Which host do u wanna delete?'},
                           Status.BAD_REQUEST)
        return respond()

    @anonymous_required
    def get(self):
        hosts = list_all_host()
        return respond([host.to_dict() for host in hosts])

    @admin_required
    def put(self, id):
        args = parse_argument('name', 'detail', 'address')
        try:
            modify_host(id, **args)
        except EmptyField as e:
            if e.field == 'id':
                return respond({'msg': 'Which host do u wanna modify?'},
                               Status.BAD_REQUEST)
            else:
                return respond(
                    {'msg': 'Required field: {field}'.format(field=e.field)},
                    Status.BAD_REQUEST)
        return respond()
