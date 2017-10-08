import unittest

from app import create_app


class FlaskAppEnvironmentMixin(unittest.TestCase):
    def setUp(self):
        app = create_app('testing')
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
