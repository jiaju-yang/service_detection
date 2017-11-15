import pytest

from app import create_app


class FlaskAppEnvironment(object):
    @pytest.fixture(scope='class')
    def app(self):
        return create_app('testing')


class FlaskAppContextEnvironment(FlaskAppEnvironment):
    @pytest.fixture
    def app_context(self, app):
        app_context = app.app_context()
        yield app_context.push()
        app_context.pop()