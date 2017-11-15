import pytest

from app.views.restful_helper import parse_argument
from tests.unit.utils import FlaskAppEnvironment


class TestParseArgument(FlaskAppEnvironment):
    def test_correct_args(self, app):
        with app.test_request_context('/?name=Peter&age=18'):
            args = parse_argument('name', {'name': 'age', 'type': int,
                                           'required': True,
                                           'dest': 'user_age'})
            assert args['name'] == 'Peter'
            assert args['user_age'] == 18

    def test_incorrect_args(self, app):
        with app.test_request_context('/?name=Peter&age=18'):
            with pytest.raises(TypeError):
                parse_argument(['name'])
