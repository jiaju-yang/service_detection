from jwt import DecodeError

from .utils import decrypt_with_jwt, now, datetime_from_str
from .entities import Anonymous, Admin, Host, Service
from .errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField

admin_repo, host_repo, service_repo = None, None, None


def _fields_required(fields, *keys):
    for key in keys:
        if not fields[key]:
            raise EmptyField(key)


def set_admin(username, original_password, sign=None,
              tip=None):
    admin = Admin(username, now(), sign, tip,
                  original_password=original_password)
    admin_repo.set(admin)


def get_tip():
    admin = admin_repo.get()
    return admin.tip


def auth_view_token(sign):
    admin = admin_repo.get()
    if not admin.is_sign_correct(sign):
        raise IncorrectSign()
    user = Anonymous(sign, now())
    return user.token()


def auth_admin_token(username, password):
    admin = admin_repo.get()
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
            admin = admin_repo.get()
            admin.auth_at = datetime_from_str(token_content['auth_at'])
            return admin
        elif role == Anonymous.role:
            return Anonymous.from_dict(token_content)
        return None


def is_valid_admin(user):
    return user and user.role == Admin.role and user.is_auth_valid()


def is_valid_anonymous(user):
    return user and user.role == Anonymous.role and user.is_auth_valid(
        admin_repo.get())


def add_host(name, detail, address):
    _fields_required(locals(), 'name', 'address')
    host = Host(name, detail, address)
    host_repo.add(host)


def delete_host(id):
    _fields_required(locals(), 'id')
    host_repo.delete(id)


def list_all_host():
    return host_repo.all()


def modify_host(id, name, detail, address):
    _fields_required(locals(), 'id', 'name', 'address')
    host = Host(name, detail, address, id=id)
    host_repo.modify(host)


def add_service(host_id, name, detail, port):
    _fields_required(locals(), 'host_id', 'name', 'port')
    service = Service(name, detail, port)
    service_repo.add(host_id, service)


def delete_service(id):
    _fields_required(locals(), 'id')
    service_repo.delete(id)


def modify_service(id, name, detail, port, host_id):
    _fields_required(locals(), 'id', 'name', 'port', 'host_id')
    service = Service(name, detail, port, id=id)
    service_repo.modify(host_id, service)
