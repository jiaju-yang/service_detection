from flask import jsonify

SUCCESS = 200
CREATED = 201

BAD_REQUEST = 400


def respond(adict=None, status=SUCCESS):
    if not adict:
        adict = {}
    response = jsonify(adict)
    response.status_code = status
    return response
