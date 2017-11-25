class SDException(Exception):
    pass


class IncorrectSign(SDException):
    pass


class IncorrectPassword(SDException):
    pass


class IncorrectUsername(SDException):
    pass


class EmptyField(SDException):
    def __init__(self, field):
        self.field = field


class NoAdministratorFound(SDException):
    pass


class RequiredPropertyNotProvided(SDException):
    pass
