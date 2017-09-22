class IncorrectSign(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class IncorrectUsername(Exception):
    pass


class EmptyField(Exception):
    def __init__(self, field):
        self.field = field
