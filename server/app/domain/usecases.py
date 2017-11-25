from jwt import DecodeError

from .assertions import assert_not_none
from .utils import decrypt_with_jwt, now, datetime_from_str
from .entities import Anonymous, Admin, Host, Service
from .errors import IncorrectSign, IncorrectUsername, IncorrectPassword, \
    EmptyField
from .registry import repos


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
    id = repos.host.next_identity()
    host = Host(id, name, detail, address)
    repos.host.save(host)


def delete_host(id):
    if not id:
        raise EmptyField('id')
    repos.host.delete(id)


def list_all_host():
    return repos.host.all()


def modify_host(id, name, detail, address):
    host = Host(id, name, detail, address)
    repos.host.save(host)


def add_service(host_id, name, detail, port):
    assert_not_none(host_id, field='host_id')
    host = repos.host.host_of_id(host_id)
    new_service = host.add_new_service(name, detail, port)
    repos.service.save(host_id, new_service)


def delete_service(id):
    assert_not_none(id, field='id')
    repos.service.delete(id)


def modify_service(id, name, detail, port, host_id):
    assert_not_none(host_id, field='host_id')
    service = Service(id, name, detail, port)
    repos.service.save(host_id, service)
