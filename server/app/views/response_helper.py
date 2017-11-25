from flask import jsonify
from enum import Enum


class Status(Enum):
    SUCCESS = (200, 'OK')
    CREATED = (201, 'Created')

    BAD_REQUEST = (400, 'Bad Request')
    UNAUTHORIZED = (401, 'Unauthorized')
    NOT_FOUND = (404, 'Not found')

    INTERNAL_SERVER_ERROR = (500, 'Internal server error')

    def __init__(self, code, default_msg):
        self.code = code
        self.default_msg = default_msg


def respond(data=None, status=Status.SUCCESS):
    if not data:
        data = {'msg': status.default_msg}
    response = jsonify(data)
    response.status_code = status.code
    return response
