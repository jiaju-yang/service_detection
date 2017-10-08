from functools import wraps
from flask import request

from .repos import AdminRepoImpl
from .domain.usecases import is_valid_admin, is_valid_anonymous
from . import status


def anonymous_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if is_valid_admin(request.user) or is_valid_anonymous(AdminRepoImpl(),
                                                              request.user):
            return func(*args, **kwargs)
        else:
            return status.respond({'msg': 'Invalid user!'}, status.UNAUTHORIZED)

    return wrap


def admin_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if is_valid_admin(request.user):
            return func(*args, **kwargs)
        else:
            return status.respond({'msg': 'Invalid administrator!'},
                                  status.UNAUTHORIZED)

    return wrap
