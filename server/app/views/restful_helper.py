from flask_restplus import reqparse


def parse_argument(*args):
    r"""

    :param args: 'a' or
    {'name': 'a',
     'dest': 'b',
     'required': True,
     'type': str}
    :return:
    """
    parser = reqparse.RequestParser()
    for arg in args:
        if isinstance(arg, str):
            parser.add_argument(arg)
        elif isinstance(arg, dict):
            parser.add_argument(**arg)
        else:
            raise TypeError('Not supported arg type: {}.'.format(str(arg)))
    return parser.parse_args()
