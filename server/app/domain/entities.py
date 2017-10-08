from .utils import encrypt_irreversibly, encrypt_with_jwt, datetime_from_str, \
    datetime_to_str, is_auth_time_valid
from .errors import EmptyField


def _fields_required(fields, *keys):
    for key in keys:
        if not fields[key]:
            raise EmptyField(key)


class Admin(object):
    role = 'admin'

    def __init__(self, username, updated_at, sign=None, tip=None, auth_at=None,
                 *, original_password=None, encrypted_password=None):
        _fields_required(locals(), 'username', 'updated_at')
        self.username = username
        self.updated_at = updated_at
        self.sign = sign
        self.tip = tip
        if not original_password and not encrypted_password:
            raise EmptyField('password')
        self.password = encrypted_password or encrypt_irreversibly(
            original_password)
        self.auth_at = auth_at

    def is_username_correct(self, username):
        return username == self.username

    def is_password_correct(self, password):
        return encrypt_irreversibly(password) == self.password

    def is_sign_correct(self, sign):
        return self.sign == sign

    def is_auth_valid(self):
        return self.auth_at and self.auth_at > self.updated_at and \
               is_auth_time_valid(self.auth_at)

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'auth_at': datetime_to_str(self.auth_at)})


class Anonymous(object):
    role = 'anonymous'

    def __init__(self, sign, auth_at):
        self.sign = sign
        self.auth_at = auth_at

    def is_auth_valid(self, admin: Admin):
        return self.auth_at and self.sign == admin.sign and \
               self.auth_at > admin.updated_at and \
               is_auth_time_valid(self.auth_at)

    @classmethod
    def from_dict(cls, adict):
        return cls(adict['sign'], datetime_from_str(adict['auth_at']))

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'sign': self.sign,
             'auth_at': datetime_to_str(self.auth_at)})


class Host(object):
    def __init__(self, name, detail, address, services=None, id=None):
        self.name = name
        self.detail = detail
        self.address = address
        self.services = []
        if services:
            self.services.extend(services)
        self.id = id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'address': self.address,
            'services': [service.to_json() for service in self.services]
        }


class Service(object):
    def __init__(self, name, detail, port, id=None):
        self.name = name
        self.detail = detail
        self.port = port
        self.id = id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'port': self.port
        }
