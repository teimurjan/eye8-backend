from src.utils.request import Request
from src.constants.headers import AUTHORIZATION_HEADER
from src.services.user import UserService


class AuthorizeHttpMiddleware:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def handle(self, request: Request):
        authorization = request.headers.get("Authorization")
        request.user = None
        if authorization is not None:
            token = authorization.replace("Bearer ", "")
            request.user = self._user_service.authorize(token)
