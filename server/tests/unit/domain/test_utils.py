import unittest
from datetime import datetime, timedelta
from flask import current_app

from app import create_app
from app.domain.utils import encrypt_with_jwt, decrypt_with_jwt, \
    datetime_from_str, datetime_to_str, auth_valid_period, is_auth_time_valid, \
    encrypt_irreversibly


class BasicFlaskAppEnvironment(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


class JWTTestCase(BasicFlaskAppEnvironment):
    def test_encryption(self):
        adict = {'name': 'psyche'}
        token = encrypt_with_jwt(adict)
        self.assertEqual(type(token), str)
        self.assertEqual(decrypt_with_jwt(token), adict)


class DatetimeTestCase(unittest.TestCase):
    def test_datetime_string_conversion(self):
        now = datetime.now()
        datetime_str = datetime_to_str(now)
        self.assertEqual(type(datetime_str), str)
        self.assertEqual(datetime_from_str(datetime_str), now)


class AuthTestCase(BasicFlaskAppEnvironment):
    def test_valid_auth_period(self):
        self.assertEqual(auth_valid_period().total_seconds(),
                         current_app.config[
                             'AUTH_VALID_PERIOD_IN_DAY'] * 3600 * 24)

    def test_valid_auth_time(self):
        self.assertTrue(is_auth_time_valid(datetime.now()))
        yesterday = datetime.now() - timedelta(days=1)
        self.assertTrue(is_auth_time_valid(yesterday))

    def test_invalid_auth_time(self):
        seven_days_ago = datetime.now() - timedelta(days=7)
        self.assertFalse(is_auth_time_valid(seven_days_ago))
        future = datetime.now() + timedelta(seconds=10)
        self.assertFalse(is_auth_time_valid(future))


class EncryptionTestCase(unittest.TestCase):
    def test_irreversible_encryption(self):
        string = 'Ah ow!2b!'
        encrypted = encrypt_irreversibly(string)
        self.assertEqual(type(encrypted), str)
        self.assertNotEqual(encrypted, string)
