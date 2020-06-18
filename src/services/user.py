import bcrypt
import jwt
from flask import current_app as app

from src.errors import NotAuthorizedError
from src.factories.token import (ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
                                 TokenFactory)


class UserService:
    def __init__(self, repo):
        self._repo = repo

    def authorize(self, token):
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'])
            return self._repo.get_by_id(decoded_token['user_id'])
        except Exception:
            raise NotAuthorizedError()

    def authenticate(self, data):
        user = self._repo.get_first_by_email(data['email'])

        if (
            user is None or
            not bcrypt.checkpw(
                data['password'].encode(),
                user.password.encode()
            )
        ):
            raise self.AuthCredsInvalid()

        return (
            TokenFactory.create(ACCESS_TOKEN_TYPE, user),
            TokenFactory.create(REFRESH_TOKEN_TYPE, user)
        )

    def refresh_token(self, data):
        try:
            decoded_token = jwt.decode(
                data['refresh_token'], app.config['SECRET_KEY']
            )
            user = self._repo.get_by_id(decoded_token['user_id'])
            return (
                TokenFactory.create(ACCESS_TOKEN_TYPE, user),
                TokenFactory.create(REFRESH_TOKEN_TYPE, user)
            )
        except (jwt.InvalidTokenError, self._repo.DoesNotExist):
            raise self.TokenInvalid()

    class AuthCredsInvalid(Exception):
        pass

    class TokenInvalid(Exception):
        pass
