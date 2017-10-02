from .utils import encrypt_irreversibly, encrypt_with_jwt, now, \
    datetime_from_str, datetime_to_str, is_auth_time_valid


class Admin(object):
    role = 'admin'

    def __init__(self, username, password, updated_at, sign=None, tip=None,
                 *, original_password=None):
        self.username = username
        self.password = password
        self.updated_at = updated_at
        self.sign = sign
        self.tip = tip
        if original_password:
            self.password = encrypt_irreversibly(original_password)
        self._auth_at = None

    @property
    def auth_at(self):
        return self._auth_at

    @auth_at.setter
    def auth_at(self, auth_at_str):
        self._auth_at = datetime_from_str(auth_at_str)

    def is_username_correct(self, username):
        return username == self.username

    def is_password_correct(self, password):
        return encrypt_irreversibly(password) == self.password

    def is_sign_correct(self, sign):
        return self.sign == sign

    def is_auth_valid(self):
        return self._auth_at and self._auth_at > self.updated_at and is_auth_time_valid(
            self._auth_at)

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'username': self.username,
             'auth_at': datetime_to_str(now())})


class Anonymous(object):
    role = 'anonymous'

    def __init__(self, sign, auth_at=None):
        self.sign = sign
        self.auth_at = auth_at

    def is_auth_valid(self, admin: Admin):
        return self.auth_at and self.sign == admin.sign and is_auth_time_valid(
            self.auth_at)

    @classmethod
    def from_dict(cls, adict):
        return cls(adict['sign'], datetime_from_str(adict['auth_at']))

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'sign': self.sign,
             'auth_at': datetime_to_str(now())})


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
