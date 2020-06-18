class InvalidEntityFormat(Exception):
    def __init__(self, errors):
        self.errors = errors

class AccessRoleError(Exception):
    pass

class NotAuthorizedError(Exception):
    pass