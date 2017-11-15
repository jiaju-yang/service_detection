from datetime import datetime, timedelta

from app.domain.entities import Admin, ToDictMixin


class TestAdmin(object):
    def test_init_with_original_password(self):
        admin_data = {'username': 'test',
                      'updated_at': datetime.now() - timedelta(
                          hours=1),
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'original_password': '123456',
                      'auth_at': datetime.now()}
        admin = Admin(**admin_data)
        assert admin.username == admin_data['username']
        assert admin.password != admin_data['original_password']
        assert admin.updated_at == admin_data['updated_at']
        assert admin.sign == admin_data['sign']
        assert admin.tip == admin_data['tip']
        assert admin.auth_at == admin_data['auth_at']

    def test_init_with_encrypted_password(self):
        admin_data = {'username': 'test',
                      'updated_at': datetime.now() - timedelta(
                          hours=1),
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'encrypted_password': '123456%DS',
                      'auth_at': datetime.now()}
        admin = Admin(**admin_data)
        assert admin.username == admin_data['username']
        assert admin.password == admin_data['encrypted_password']
        assert admin.updated_at == admin_data['updated_at']
        assert admin.sign == admin_data['sign']
        assert admin.tip == admin_data['tip']
        assert admin.auth_at == admin_data['auth_at']


class Point(ToDictMixin):
    _dict_fields = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line(ToDictMixin):
    _dict_fields = ('start', 'end')

    def __init__(self, start, end):
        self.start = start
        self.end = end


class Square(ToDictMixin):
    _dict_fields = ('vertexes',)

    def __init__(self, vertexes):
        self.vertexes = vertexes


class ToDictMixinTestCase(object):
    def test_single_object(self):
        point_data = {'x': 3, 'y': 4}
        point = Point(**point_data)
        assert point.to_dict() == point_data

    def test_nested_object(self):
        start_point_data = {'x': 0, 'y': 1}
        end_point_data = {'x': 3, 'y': 4}
        line_data = {'start': {'x': 0, 'y': 1}, 'end': {'x': 3, 'y': 4}}
        line = Line(Point(**start_point_data),
                    Point(**end_point_data))
        assert line.to_dict() == line_data

    def test_builtin_data_structure(self):
        square_data = {
            'vertexes': [{'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 0, 'y': 1},
                         {'x': 0, 'y': 0}]}
        square = Square(**square_data)
        assert square.to_dict() == square_data

        square_data = {
            'vertexes': {'first': {'x': 1, 'y': 0}, 'second': {'x': 1, 'y': 1},
                         'third': {'x': 0, 'y': 1}, 'fourth': {'x': 0, 'y': 0}}}
        square = Square(**square_data)
        assert square.to_dict() == square_data

    def test_alias(self):
        class GeoPoint(Point):
            _dict_fields = (('x', 'lng'), ('y', 'lat'))

        point_data = {'lng': 1, 'lat': 2}
        point = GeoPoint(point_data['lng'], point_data['lat'])
        assert point.to_dict() == point_data
