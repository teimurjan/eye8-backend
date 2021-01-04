from src.errors import AccessRoleError, NotAuthorizedError


def allow_roles(allowed_roles):
    def _allow_roles(f):
        def wrapper(self, *args, **kwargs):
            user = kwargs.get("user")
            if user is None:
                raise NotAuthorizedError()
            if user.group.name not in allowed_roles:
                raise AccessRoleError()
            return f(self, *args, **kwargs)

        return wrapper

    return _allow_roles
