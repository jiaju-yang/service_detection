from flask import jsonify


SUCCESS = 200
BAD_REQUEST = 400


def respond(adict, status=SUCCESS):
    response = jsonify(adict)
    response.status_code = status
    return response
