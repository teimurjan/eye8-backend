from src.validation_rules.authentication import AuthenticationData
from src.repos.user import UserRepo
import bcrypt
import jwt
from flask import current_app as app

from src.errors import NotAuthenticatedError
from src.factories.token import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TokenFactory


class UserService:
    def __init__(self, repo: UserRepo):
        self._repo = repo

    def authorize(self, token: str):
        try:
            decoded_token = jwt.decode(token, app.config["SECRET_KEY"])
            return self._repo.get_by_id(decoded_token["user_id"])
        except Exception as e:
            raise NotAuthenticatedError()

    def authenticate(self, data: AuthenticationData):
        user = self._repo.get_first_by_email(data["email"])

        if user is None or not bcrypt.checkpw(
            data["password"].encode(), user.password.encode()
        ):
            raise self.AuthCredsInvalid()

        return (
            TokenFactory.create(ACCESS_TOKEN_TYPE, user),
            TokenFactory.create(REFRESH_TOKEN_TYPE, user),
        )

    def refresh_token(self, refresh_token: str):
        try:
            decoded_token = jwt.decode(refresh_token, app.config["SECRET_KEY"])
            user = self._repo.get_by_id(decoded_token["user_id"])
            return (
                TokenFactory.create(ACCESS_TOKEN_TYPE, user),
                TokenFactory.create(REFRESH_TOKEN_TYPE, user),
            )
        except (jwt.InvalidTokenError, self._repo.DoesNotExist):
            raise self.TokenInvalid()

    class AuthCredsInvalid(Exception):
        pass

    class TokenInvalid(Exception):
        pass
