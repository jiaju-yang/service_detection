from jwt import DecodeError

from .utils import decrypt_with_jwt, now, datetime_from_str
from .entities import Anonymous, Admin, Host, Service
from .errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField
from .repos import repos


def _fields_required(fields, *keys):
    for key in keys:
        if not fields[key]:
            raise EmptyField(key)


def set_admin(username, original_password, sign=None,
              tip=None):
    admin = Admin(username, now(), sign, tip,
                  original_password=original_password)
    repos.admin.set(admin)


def get_tip():
    admin = repos.admin.get()
    return admin.tip


def auth_view_token(sign):
    admin = repos.admin.get()
    if not admin.is_sign_correct(sign):
        raise IncorrectSign()
    user = Anonymous(sign, now())
    return user.token()


def auth_admin_token(username, password):
    admin = repos.admin.get()
    if not admin.is_username_correct(username):
        raise IncorrectUsername()
    if not admin.is_password_correct(password):
        raise IncorrectPassword()
    admin.auth_at = now()
    return admin.token()


def get_user_by_token(token):
    if not token:
        return None
    try:
        token_content = decrypt_with_jwt(token)
    except DecodeError:
        return None
    else:
        role = token_content.get('role', None)
        if role == Admin.role:
            admin = repos.admin.get()
            admin.auth_at = datetime_from_str(token_content['auth_at'])
            return admin
        elif role == Anonymous.role:
            return Anonymous.from_dict(token_content)
        return None


def is_valid_admin(user):
    return user and user.role == Admin.role and user.is_auth_valid()


def is_valid_anonymous(user):
    return user and user.role == Anonymous.role and user.is_auth_valid(
        repos.admin.get())


def add_host(name, detail, address):
    host = Host(name, detail, address)
    repos.host.add(host)


def delete_host(id):
    _fields_required(locals(), 'id')
    repos.host.delete(id)


def list_all_host():
    return repos.host.all()


def modify_host(id, name, detail, address):
    _fields_required(locals(), 'id')
    host = Host(name, detail, address, id=id)
    repos.host.modify(host)


def add_service(host_id, name, detail, port):
    _fields_required(locals(), 'host_id')
    service = Service(name, detail, port)
    repos.service.add(host_id, service)


def delete_service(id):
    _fields_required(locals(), 'id')
    repos.service.delete(id)


def modify_service(id, name, detail, port, host_id):
    _fields_required(locals(), 'id', 'host_id')
    service = Service(name, detail, port, id=id)
    repos.service.modify(host_id, service)
