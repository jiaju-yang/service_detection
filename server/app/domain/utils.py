from datetime import datetime, timedelta
from hashlib import sha256
import jwt
from flask import current_app

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def now():
    return datetime.now()


def datetime_to_str(datetime):
    return datetime.strftime(TIME_FORMAT)


def datetime_from_str(string):
    return datetime.strptime(string, TIME_FORMAT)


def auth_valid_period():
    return timedelta(days=current_app.config['AUTH_VALID_PERIOD_IN_DAY'])


def encrypt_irreversibly(string):
    algo = sha256()
    algo.update(string.encode(encoding='utf-8'))
    return algo.hexdigest()


def encrypt_with_jwt(adict):
    secret_key = current_app.config['SECRET_KEY']
    return jwt.encode(adict, secret_key, algorithm='HS256').decode(encoding='utf-8')


def decrypt_with_jwt(token):
    secret_key = current_app.config['SECRET_KEY']
    return jwt.decode(token.encode(encoding='utf-8'), secret_key, algorithms=['HS256'])

