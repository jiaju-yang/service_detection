import unittest
from flask import Flask

from app.views.restful_helper import parse_argument


class ParseArgumentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    def test_correct_args(self):
        with self.app.test_request_context('/?name=Peter&age=18'):
            args = parse_argument('name', {'name': 'age', 'type': int,
                                           'required': True, 'dest': 'user_age'})
            self.assertEqual(args['name'], 'Peter')
            self.assertEqual(args['user_age'], 18)

    def test_incorrect_args(self):
        with self.app.test_request_context('/?name=Peter&age=18'):
            self.assertRaises(TypeError, parse_argument, ['name'])


