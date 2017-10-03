import unittest
from datetime import datetime, timedelta
from flask import current_app

from app import create_app
from app.domain.utils import encrypt_with_jwt, decrypt_with_jwt, \
    datetime_from_str, datetime_to_str, auth_valid_period, is_auth_time_valid, \
    encrypt_irreversibly


class JWTTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_encryption(self):
        with self.app.app_context():
            adict = {'name': 'psyche'}
            token = encrypt_with_jwt(adict)
            self.assertEqual(type(token), str)
            self.assertEqual(decrypt_with_jwt(token), adict)


class DatetimeTestCase(unittest.TestCase):
    def test_datetime_string_conversion(self):
        now = datetime.now()
        self.assertEqual(datetime_from_str(datetime_to_str(now)), now)


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_valid_auth_period(self):
        with self.app.app_context():
            self.assertEqual(auth_valid_period().total_seconds(),
                             current_app.config[
                                 'AUTH_VALID_PERIOD_IN_DAY'] * 3600 * 24)

    def test_valid_auth_time(self):
        with self.app.app_context():
            self.assertTrue(is_auth_time_valid(datetime.now()))
            yesterday = datetime.now() - timedelta(days=1)
            self.assertTrue(is_auth_time_valid(yesterday))

    def test_invalid_auth_time(self):
        with self.app.app_context():
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
