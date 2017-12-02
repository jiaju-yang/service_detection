from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from flask import current_app

from app import domain
from app.domain.entities import Admin, Anonymous, Host
from app.domain.errors import (IncorrectSign, IncorrectUsername,
                               IncorrectPassword, EmptyField)
from app.domain.usecases import (
    set_admin, get_tip, auth_view_token, auth_admin_token, get_user_by_token,
    is_valid_admin, is_valid_anonymous, add_host, delete_host, list_all_host,
    modify_host, add_service, delete_service, modify_service)
from tests.unit.utils import FlaskAppContextEnvironment


@pytest.fixture
def admin_data():
    return {'username': 'test',
            'updated_at': datetime.now() - timedelta(days=2),
            'sign': 'bullshit',
            'tip': 'How\'s the code?',
            'original_password': '123456',
            'auth_at': datetime.now() - timedelta(days=1)}


@pytest.fixture
def anonymous_data():
    return {'sign': 'bullshit',
            'auth_at': datetime.now() - timedelta(days=1)}


@pytest.fixture
def admin_repo():
    repo = Mock()
    repo.set = Mock()
    repo.get = Mock()
    domain.inject_repos(admin=repo)
    return repo


@pytest.fixture
def host_repo():
    repo = Mock()
    repo.next_identity = Mock()
    repo.save = Mock()
    repo.delete = Mock()
    repo.all = Mock()
    repo.host_of_id = Mock()
    domain.inject_repos(host=repo)
    return repo


@pytest.fixture
def service_repo():
    repo = Mock()
    repo.add = Mock()
    repo.delete = Mock()
    repo.modify = Mock()
    domain.inject_repos(service=repo)
    return repo


class TestSetAdmin(object):
    @pytest.fixture
    def admin_data(self):
        return {'username': 'test',
                'sign': 'bullshit',
                'tip': 'How\'s the code?',
                'original_password': '123456'}

    def test_success_set(self, admin_repo, admin_data):
        set_admin(**admin_data)
        admin_repo.set.assert_called_once()

    @pytest.mark.parametrize(
        'username, sign, tip, original_password, expected', [
            ['', 'bullshit', 'How\'s the code?', '123456', 'username'],
            ['test', 'bullshit', 'How\'s the code?', '', 'password']])
    def test_required_fields(self, username, sign, tip, original_password,
                             expected):
        with pytest.raises(EmptyField) as exc_info:
            set_admin(username, original_password, sign, tip)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == expected


def test_get_tip(admin_repo, admin_data):
    admin_repo.get.return_value = Admin(**admin_data)
    assert get_tip() == admin_data['tip']


@pytest.fixture
def set_repo_get(admin_repo, admin_data):
    admin_repo.get.return_value = Admin(**admin_data)


class TestAuthViewToken(FlaskAppContextEnvironment):
    def test_success_auth(self, app_context, set_repo_get, admin_data):
        assert type(auth_view_token(admin_data['sign'])) is str

    def test_fail_auth(self, app_context):
        with pytest.raises(IncorrectSign):
            auth_view_token('What\'s your name?')


class TestAuthAdminToken(FlaskAppContextEnvironment):
    def test_success_auth(self, app_context, set_repo_get, admin_data):
        assert type(auth_admin_token(admin_data['username'],
                                     admin_data['original_password'])) is str

    def test_incorrect_username_auth(self, app_context, set_repo_get,
                                     admin_data):
        with pytest.raises(IncorrectUsername):
            auth_admin_token('What\'s your name?', admin_data[
                'original_password'])

    def test_incorrect_password_auth(self, app_context, set_repo_get,
                                     admin_data):
        with pytest.raises(IncorrectPassword):
            auth_admin_token(admin_data['username'], '123456xd')


class TestGetUserByToken(FlaskAppContextEnvironment):
    @pytest.mark.parametrize(
        'invalid_token', [None, '', 'abc'])
    def test_invalid_token(self, app_context, set_repo_get, invalid_token):
        assert get_user_by_token(invalid_token) is None

    def test_anonymous_token(self, app_context, set_repo_get, admin_data,
                             anonymous_data):
        token = Anonymous(**anonymous_data).token()
        user = get_user_by_token(token)
        assert user.sign == admin_data['sign']
        assert user.auth_at == anonymous_data['auth_at']
        assert user.role == Anonymous.role

    def test_admin_token(self, app_context, set_repo_get, admin_data):
        token = Admin(**admin_data).token()
        user = get_user_by_token(token)
        assert user.username == admin_data['username']
        assert user.auth_at == admin_data['auth_at']
        assert user.role == Admin.role


class TestValidAdmin(FlaskAppContextEnvironment):
    def test_valid_admin(self, app_context, set_repo_get, admin_data):
        user = Admin(**admin_data)
        assert is_valid_admin(user)

    def test_empty_user(self, app_context, set_repo_get):
        assert not is_valid_admin(None)

    def test_anonymous(self, app_context, set_repo_get, anonymous_data):
        user = Anonymous(**anonymous_data)
        assert not is_valid_admin(user)

    def test_outdated_admin(self, app_context, set_repo_get, admin_data):
        admin_data['auth_at'] = datetime.now() - timedelta(
            days=current_app.config['AUTH_VALID_PERIOD_IN_DAY'] + 1)
        user = Admin(**admin_data)
        assert not is_valid_admin(user)

    def test_updated_admin(self, app_context, set_repo_get, admin_data):
        admin_data['updated_at'] = datetime.now() - timedelta(hours=12)
        user = Admin(**admin_data)
        assert not is_valid_admin(user)


class TestIsValidAnonymous(FlaskAppContextEnvironment):
    def test_valid_anonymous(self, app_context, set_repo_get, anonymous_data):
        user = Anonymous(**anonymous_data)
        assert is_valid_anonymous(user)

    def test_empty_user(self, app_context, set_repo_get):
        assert not is_valid_anonymous(None)

    def test_admin(self, app_context, set_repo_get, admin_data):
        user = Admin(**admin_data)
        assert not is_valid_anonymous(user)

    def test_outdated_anonymous(self, app_context, set_repo_get,
                                anonymous_data):
        anonymous_data['auth_at'] = datetime.now() - timedelta(
            days=current_app.config['AUTH_VALID_PERIOD_IN_DAY'] + 1)
        user = Anonymous(**anonymous_data)
        assert not is_valid_anonymous(user)

    def test_updated_admin(self, app_context, set_repo_get, admin_repo,
                           anonymous_data):
        admin_repo.get.return_value.updated_at = datetime.now() - timedelta(
            hours=12)
        user = Anonymous(**anonymous_data)
        assert not is_valid_anonymous(user)


class TestSaveHost(object):
    def test_success_save(self, host_repo):
        add_host('localhost', 'this machine', '127.0.0.1')
        host_repo.save.assert_called_once()

    @pytest.mark.parametrize(
        'host_data, expected',
        [[['', '', '127.0.0.1'], 'name'], [['localhost', '', ''], 'address']])
    def test_fail_add(self, host_repo, host_data, expected):
        with pytest.raises(EmptyField) as exc_info:
            add_host(*host_data)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == expected


class TestDeleteHost(object):
    def test_success_delete(self, host_repo):
        delete_host(1)
        host_repo.delete.assert_called_once()

    def test_empty_id(self, host_repo):
        with pytest.raises(EmptyField) as exc_info:
            delete_host(None)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == 'id'


def test_list_host(host_repo):
    list_all_host()
    host_repo.all.assert_called_once()


class TestModifyHost(object):
    def test_success_modify(self, host_repo):
        modify_host(1, 'localhost', '', '127.0.0.1')
        host_repo.save.assert_called_once()

    @pytest.mark.parametrize(
        'host_data, expected',
        [[[None, 'localhost', '', '127.0.0.1'], 'id'],
         [[1, '', '', '127.0.0.1'], 'name'],
         [[1, 'localhost', '', ''], 'address']])
    def test_fail_modify(self, host_repo, host_data, expected):
        with pytest.raises(EmptyField) as exc_info:
            modify_host(*host_data)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == expected


class TestAddService(object):
    def test_success_save(self, service_repo, host_repo):
        add_service(1, 'nginx', 'nginx for website', 80)
        service_repo.save.assert_called_once()

    @pytest.mark.parametrize(
        'service_data, expected',
        [[[None, 'nginx', 'nginx for website', 80], 'host_id'],
         [[1, '', 'nginx for website', 80], 'name'],
         [[1, 'nginx', 'nginx for website', None], 'port']])
    def test_fail_add(self, host_repo, service_repo, service_data, expected):
        host_repo.host_of_id.return_value = Host('fake_1', 'xxx', 'yyy', 'zzz')
        with pytest.raises(EmptyField) as exc_info:
            add_service(*service_data)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == expected


class TestDeleteService(object):
    def test_success_delete(self, service_repo):
        delete_service(1)
        service_repo.delete.assert_called_once()

    def test_empty_id(self, service_repo):
        with pytest.raises(EmptyField) as exc_info:
            delete_service(None)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == 'id'


class TestModifyService(object):
    def test_success_modify(self, service_repo):
        modify_service(1, 'nginx', '', 80, 2)
        service_repo.save.assert_called_once()

    @pytest.mark.parametrize(
        'service_data, expected',
        [[[None, 'nginx', '', 80, 2], 'id'],
         [[1, '', '', 80, 2], 'name'],
         [[1, 'nginx', '', None, 2], 'port'],
         [[1, 'nginx', '', 80, None], 'host_id']])
    def test_fail_modify(self, service_repo, service_data, expected):
        with pytest.raises(EmptyField) as exc_info:
            modify_service(*service_data)
        assert exc_info.type is EmptyField
        assert exc_info.value.field == expected
