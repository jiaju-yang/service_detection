from functools import wraps
from flask import request

from .domain.usecases import is_valid_admin
from . import status


def anonymous_required(func):
    pass


def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if is_valid_admin(request.user):
            return func(*args, **kwargs)
        else:
            return status.respond({'msg': 'Invalid administrator!'}, status.BAD_REQUEST)
    return wrap
