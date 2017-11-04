from unittest import TestCase
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from flask import current_app

from app import domain
from app.domain.entities import Admin, Anonymous
from app.domain.errors import (IncorrectSign, IncorrectUsername,
                               IncorrectPassword, EmptyField)
from app.domain.usecases import (
    set_admin, get_tip, auth_view_token, auth_admin_token, get_user_by_token,
    is_valid_admin, is_valid_anonymous, add_host, delete_host, list_all_host,
    modify_host, add_service, delete_service, modify_service)
from app.domain.repos import AdminRepo, HostRepo, ServiceRepo
from tests.unit.utils import FlaskAppEnvironmentMixin


class MockRepoFactory(object):
    @classmethod
    @patch.multiple(AdminRepo, __abstractmethods__=set())
    def admin(cls):
        repo = AdminRepo()
        repo.set = Mock()
        repo.get = Mock()
        return repo

    @classmethod
    @patch.multiple(HostRepo, __abstractmethods__=set())
    def host(cls):
        repo = HostRepo()
        repo.add = Mock()
        repo.delete = Mock()
        repo.all = Mock()
        repo.modify = Mock()
        return repo

    @classmethod
    @patch.multiple(ServiceRepo, __abstractmethods__=set())
    def service(cls):
        repo = ServiceRepo()
        repo.add = Mock()
        repo.delete = Mock()
        repo.modify = Mock()
        return repo


class MockData(object):
    @classmethod
    def admin(cls):
        return {'username': 'test',
                'updated_at': datetime.now() - timedelta(days=2),
                'sign': 'bullshit',
                'tip': 'How\'s the code?',
                'original_password': '123456',
                'auth_at': datetime.now() - timedelta(days=1)}

    @classmethod
    def anonymous(cls):
        return {'sign': 'bullshit',
                'auth_at': datetime.now() - timedelta(days=1)}


class SetAdminTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.admin()
        domain.inject_repos(admin=self.repo)

    def test_success_set(self):
        admin_data = {'username': 'test',
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'original_password': '123456'}
        set_admin(**admin_data)
        self.repo.set.assert_called_once()

    def test_empty_username(self):
        admin_data = {'username': '',
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'original_password': '123456'}
        with self.assertRaises(EmptyField) as cm:
            set_admin(**admin_data)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'username')

    def test_empty_password(self):
        admin_data = {'username': 'test',
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'original_password': ''}
        with self.assertRaises(EmptyField) as cm:
            set_admin(**admin_data)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'password')


class GetTipTestCase(TestCase):
    def setUp(self):
        repo = MockRepoFactory.admin()
        self.admin_data = MockData.admin()
        repo.get.return_value = Admin(**self.admin_data)
        domain.inject_repos(admin=repo)

    def test_get_tip(self):
        self.assertEqual(get_tip(), self.admin_data['tip'])


class AuthViewTokenTestCase(FlaskAppEnvironmentMixin):
    def setUp(self):
        super().setUp()
        repo = MockRepoFactory.admin()
        self.admin_data = MockData.admin()
        repo.get.return_value = Admin(**self.admin_data)
        domain.inject_repos(admin=repo)

    def test_success_auth(self):
        self.assertEqual(
            type(auth_view_token(self.admin_data['sign'])), str)

    def test_fail_auth(self):
        self.assertRaises(IncorrectSign, auth_view_token,
                          'What\'s your name?')


class AuthAdminTokenTestCase(FlaskAppEnvironmentMixin):
    def setUp(self):
        super().setUp()
        repo = MockRepoFactory.admin()
        self.admin_data = MockData.admin()
        repo.get.return_value = Admin(**self.admin_data)
        domain.inject_repos(admin=repo)

    def test_success_auth(self):
        self.assertEqual(
            type(auth_admin_token(self.admin_data['username'],
                                  self.admin_data[
                                      'original_password'])), str)

    def test_incorrect_username_auth(self):
        self.assertRaises(IncorrectUsername, auth_admin_token,
                          'What\'s your name?', self.admin_data[
                              'original_password'])

    def test_incorrect_password_auth(self):
        self.assertRaises(IncorrectPassword, auth_admin_token,
                          self.admin_data['username'], '123456xd')


class GetUserByTokenTestCase(FlaskAppEnvironmentMixin):
    def setUp(self):
        super().setUp()
        repo = MockRepoFactory.admin()
        self.admin_data = MockData.admin()
        repo.get.return_value = Admin(**self.admin_data)
        domain.inject_repos(admin=repo)

    def test_invalid_token(self):
        self.assertIsNone(get_user_by_token(None))
        self.assertIsNone(get_user_by_token(''))
        self.assertIsNone(get_user_by_token('abc'))

    def test_anonymous_token(self):
        anonymous_data = MockData.anonymous()
        token = Anonymous(**anonymous_data).token()
        user = get_user_by_token(token)
        self.assertEqual(user.sign, self.admin_data['sign'])
        self.assertEqual(user.auth_at, anonymous_data['auth_at'])
        self.assertEqual(user.role, Anonymous.role)

    def test_admin_token(self):
        token = Admin(**self.admin_data).token()
        user = get_user_by_token(token)
        self.assertEqual(user.username, self.admin_data['username'])
        self.assertEqual(user.auth_at, self.admin_data['auth_at'])
        self.assertEqual(user.role, Admin.role)


class IsValidAdminTestCase(FlaskAppEnvironmentMixin):
    def test_valid_admin(self):
        admin_data = MockData.admin()
        user = Admin(**admin_data)
        self.assertTrue(is_valid_admin(user))

    def test_empty_user(self):
        self.assertFalse(is_valid_admin(None))

    def test_anonymous(self):
        anonymous_data = MockData.anonymous()
        user = Anonymous(**anonymous_data)
        self.assertFalse(is_valid_admin(user))

    def test_outdated_admin(self):
        admin_data = MockData.admin()
        admin_data['auth_at'] = datetime.now() - timedelta(
            days=current_app.config['AUTH_VALID_PERIOD_IN_DAY'] + 1)
        user = Admin(**admin_data)
        self.assertFalse(is_valid_admin(user))

    def test_updated_admin(self):
        admin_data = MockData.admin()
        admin_data['updated_at'] = datetime.now() - timedelta(hours=12)
        user = Admin(**admin_data)
        self.assertFalse(is_valid_admin(user))


class IsValidAnonymousTestCase(FlaskAppEnvironmentMixin):
    def setUp(self):
        super().setUp()
        self.repo = MockRepoFactory.admin()
        self.admin_data = MockData.admin()
        self.repo.get.return_value = Admin(**self.admin_data)
        domain.inject_repos(admin=self.repo)

    def test_valid_anonymous(self):
        anonymous_data = MockData.anonymous()
        user = Anonymous(**anonymous_data)
        self.assertTrue(is_valid_anonymous(user))

    def test_empty_user(self):
        self.assertFalse(is_valid_anonymous(None))

    def test_admin(self):
        admin_data = MockData.admin()
        user = Admin(**admin_data)
        self.assertFalse(is_valid_anonymous(user))

    def test_outdated_anonymous(self):
        anonymous_data = MockData.anonymous()
        anonymous_data['auth_at'] = datetime.now() - timedelta(
            days=current_app.config['AUTH_VALID_PERIOD_IN_DAY'] + 1)
        user = Anonymous(**anonymous_data)
        self.assertFalse(is_valid_anonymous(user))

    def test_updated_admin(self):
        self.repo.get.return_value.updated_at = datetime.now() - timedelta(
            hours=12)
        anonymous_data = MockData.anonymous()
        user = Anonymous(**anonymous_data)
        self.assertFalse(is_valid_anonymous(user))


class AddHostTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.host()
        domain.inject_repos(host=self.repo)

    def test_success_add(self):
        add_host('localhost', 'this machine', '127.0.0.1')
        self.repo.add.assert_called_once()

    def test_empty_name(self):
        with self.assertRaises(EmptyField) as cm:
            add_host('', '', '127.0.0.1')
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'name')

    def test_empty_address(self):
        with self.assertRaises(EmptyField) as cm:
            add_host('localhost', '', '')
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'address')


class DeleteHostTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.host()
        domain.inject_repos(host=self.repo)

    def test_success_delete(self):
        delete_host(1)
        self.repo.delete.assert_called_once()

    def test_empty_id(self):
        with self.assertRaises(EmptyField) as cm:
            delete_host(None)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'id')


class ListHostTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.host()
        domain.inject_repos(host=self.repo)

    def test_success_list(self):
        list_all_host()
        self.repo.all.assert_called_once()


class ModifyHostTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.host()
        domain.inject_repos(host=self.repo)

    def test_success_modify(self):
        modify_host(1, 'localhost', '', '127.0.0.1')
        self.repo.modify.assert_called_once()

    def test_empty_id(self):
        with self.assertRaises(EmptyField) as cm:
            modify_host(None, 'localhost', '', '127.0.0.1')
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'id')

    def test_empty_name(self):
        with self.assertRaises(EmptyField) as cm:
            modify_host(1, '', '', '127.0.0.1')
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'name')

    def test_empty_address(self):
        with self.assertRaises(EmptyField) as cm:
            modify_host(1, 'localhost', '', '')
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'address')


class AddServiceTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.service()
        domain.inject_repos(service=self.repo)

    def test_success_add(self):
        add_service(1, 'nginx', 'nginx for website', 80)
        self.repo.add.assert_called_once()

    def test_empty_host_id(self):
        with self.assertRaises(EmptyField) as cm:
            add_service(None, 'nginx', 'nginx for website', 80)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'host_id')

    def test_empty_name(self):
        with self.assertRaises(EmptyField) as cm:
            add_service(1, '', 'nginx for website', 80)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'name')

    def test_empty_port(self):
        with self.assertRaises(EmptyField) as cm:
            add_service(1, 'nginx', 'nginx for website', None)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'port')


class DeleteServiceTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.service()
        domain.inject_repos(service=self.repo)

    def test_success_delete(self):
        delete_service(1)
        self.repo.delete.assert_called_once()

    def test_empty_id(self):
        with self.assertRaises(EmptyField) as cm:
            delete_service(None)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'id')


class ModifyServiceTestCase(TestCase):
    def setUp(self):
        self.repo = MockRepoFactory.service()
        domain.inject_repos(service=self.repo)

    def test_success_modify(self):
        modify_service(1, 'nginx', '', 80, 2)
        self.repo.modify.assert_called_once()

    def test_empty_id(self):
        with self.assertRaises(EmptyField) as cm:
            modify_service(None, 'nginx', '', 80, 2)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'id')

    def test_empty_name(self):
        with self.assertRaises(EmptyField) as cm:
            modify_service(1, '', '', 80, 2)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'name')

    def test_empty_port(self):
        with self.assertRaises(EmptyField) as cm:
            modify_service(1, 'nginx', '', None, 2)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'port')

    def test_empty_host_id(self):
        with self.assertRaises(EmptyField) as cm:
            modify_service(1, 'nginx', '', 80, None)
        this_exception = cm.exception
        self.assertEqual(this_exception.field, 'host_id')
