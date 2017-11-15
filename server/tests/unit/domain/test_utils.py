from datetime import datetime, timedelta
from flask import current_app

from tests.unit.utils import FlaskAppContextEnvironment
from app.domain.utils import (encrypt_with_jwt, decrypt_with_jwt,
                              datetime_from_str, datetime_to_str,
                              auth_valid_period, is_auth_time_valid,
                              encrypt_irreversibly)


class TestJWT(FlaskAppContextEnvironment):
    def test_encryption(self, app_context):
        adict = {'name': 'test'}
        token = encrypt_with_jwt(adict)
        assert type(token) == str
        assert decrypt_with_jwt(token) == adict


def test_datetime_string_conversion():
    now = datetime.now()
    datetime_str = datetime_to_str(now)
    assert type(datetime_str) == str
    assert datetime_from_str(datetime_str) == now


class TestAuth(FlaskAppContextEnvironment):
    def test_valid_auth_period(self, app_context):
        assert auth_valid_period().total_seconds() == current_app.config[
                                                          'AUTH_VALID_PERIOD_IN_DAY'] * 3600 * 24

    def test_valid_auth_time(self, app_context):
        assert is_auth_time_valid(datetime.now())
        yesterday = datetime.now() - timedelta(days=1)
        assert is_auth_time_valid(yesterday)

    def test_invalid_auth_time(self, app_context):
        seven_days_ago = datetime.now() - timedelta(days=7)
        assert not is_auth_time_valid(seven_days_ago)
        future = datetime.now() + timedelta(seconds=10)
        assert not is_auth_time_valid(future)


def test_irreversible_encryption():
    string = 'Ah ow!2b!'
    encrypted = encrypt_irreversibly(string)
    assert type(encrypted) is str
    assert encrypted != string
