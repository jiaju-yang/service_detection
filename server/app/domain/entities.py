from .utils import encrypt_irreversibly, encrypt_with_jwt, now, \
    datetime_from_str, datetime_to_str, auth_valid_period


class Admin(object):
    role = 'admin'

    def __init__(self, username, password, updated_at, sign=None, tip=None,
                 *, original_password=None):
        self._username = username
        self._password = password
        self._updated_at = updated_at
        self._sign = sign
        self._tip = tip
        if original_password:
            self._password = encrypt_irreversibly(original_password)
        self._auth_at = None

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def sign(self):
        return self._sign

    @property
    def tip(self):
        return self._tip

    @property
    def auth_at(self):
        return self._auth_at

    @auth_at.setter
    def auth_at(self, auth_at):
        self._auth_at = datetime_from_str(auth_at)

    @property
    def updated_at(self):
        return self._updated_at

    def is_username_correct(self, username):
        return username == self.username

    def is_password_correct(self, password):
        return encrypt_irreversibly(password) == self.password

    def is_sign_correct(self, sign):
        return True if self._sign == sign else False

    def is_auth_valid(self):
        if not self._auth_at:
            return False
        now_time = now()
        return now_time - auth_valid_period() < self._auth_at < now_time

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'username': self.username,
             'auth_at': datetime_to_str(now())})


class AnonymousUser(object):
    role = 'anonymous'

    def __init__(self, sign, auth_at=None):
        self._sign = sign
        self._auth_at = auth_at

    def has_view_permission(self, admin: Admin):
        # if not admin.sign:
        #     return True
        # if self._token == admin.sign:
        #     return True
        # return False
        pass

    @classmethod
    def from_dict(cls, adict):
        return cls(adict['sign'], datetime_from_str(adict['auth_at']))

    def token(self):
        return encrypt_with_jwt(
            {'role': self.role, 'sign': self._sign,
             'auth_at': datetime_to_str(now())})


class Host(object):
    def __init__(self, id, name, detail, address, services):
        pass