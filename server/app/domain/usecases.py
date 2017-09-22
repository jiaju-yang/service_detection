from jwt import DecodeError

from .repos import AdminRepo, HostRepo, ServiceRepo
from .utils import decrypt_with_jwt, now
from .entities import AnonymousUser, Admin, Host, Service
from .errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField


def _fields_required(fields, *keys):
    for key in keys:
        if not fields[key]:
            raise EmptyField(key)


def auth_view_token(repo: AdminRepo, sign):
    admin = repo.get()
    if not admin.is_sign_correct(sign):
        raise IncorrectSign()
    user = AnonymousUser(sign)
    return user.token()


def auth_admin_token(repo: AdminRepo, username, password):
    admin = repo.get()
    if not admin.is_username_correct(username):
        raise IncorrectUsername()
    if not admin.is_password_correct(password):
        raise IncorrectPassword()
    return admin.token()


def get_user_by_token(repo: AdminRepo, token):
    if not token:
        return None
    try:
        token_content = decrypt_with_jwt(token)
    except DecodeError:
        return None
    else:
        role = token_content.get('role', None)
        if role == Admin.role:
            admin = repo.get()
            admin.auth_at = token_content['auth_at']
            return admin
        elif role == AnonymousUser.role:
            return AnonymousUser.from_dict(token_content)
        return None


def set_admin(repo: AdminRepo, username, original_password, sign=None,
              tip=None):
    admin = Admin(username, None, now(), sign, tip,
                  original_password=original_password)
    repo.set(admin)


def is_valid_admin(user):
    return user and user.role == Admin.role and user.is_auth_valid()


def add_host(repo: HostRepo, name, detail, address):
    _fields_required(locals(), 'name', 'address')
    host = Host(name, detail, address)
    repo.add(host)


def delete_host(repo: HostRepo, id):
    _fields_required(locals(), 'id')
    repo.delete(id)


def list_all_host(repo: HostRepo):
    return repo.all()


def modify_host(repo: HostRepo, id, name, detail, address):
    _fields_required(locals(), 'id', 'name', 'address')
    host = Host(name, detail, address, id=id)
    repo.modify(host)


def add_service(repo: ServiceRepo, host_id, name, detail, port):
    _fields_required(locals(), 'host_id', 'name', 'port')
    service = Service(name, detail, port)
    repo.add(host_id, service)


def delete_service(repo: ServiceRepo, id):
    _fields_required(locals(), 'id')
    repo.delete(id)


def modify_service(repo: ServiceRepo, id, name, detail, port, host_id):
    _fields_required(locals(), 'id', 'name', 'port', 'host_id')
    service = Service(name, detail, port, id=id)
    repo.modify(host_id, service)
