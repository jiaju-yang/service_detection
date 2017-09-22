from flask import jsonify

SUCCESS = 200
CREATED = 201

BAD_REQUEST = 400


def respond(data=None, status=SUCCESS):
    if not data:
        data = {}
    response = jsonify(data)
    response.status_code = status
    return response
