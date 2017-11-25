from functools import wraps

from flask import request

from app.domain.usecases import is_valid_admin, is_valid_anonymous
from .response_helper import Status, respond


def anonymous_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if is_valid_admin(request.user) or is_valid_anonymous(request.user):
            return func(*args, **kwargs)
        else:
            return respond({'msg': 'Invalid user!'}, Status.UNAUTHORIZED)

    return wrap


def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if is_valid_admin(request.user):
            return func(*args, **kwargs)
        else:
            return respond({'msg': 'Invalid administrator!'},
                           Status.UNAUTHORIZED)

    return wrap
