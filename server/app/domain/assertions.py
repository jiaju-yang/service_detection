from .errors import EmptyField


def assert_not_none(argument, field=''):
    if not argument:
        raise EmptyField(field)
