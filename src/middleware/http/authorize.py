from src.utils.request import Request
from src.services.user import UserService


class AuthorizeHttpMiddleware:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def handle(self, request: Request):
        authorization = request.headers.get("Authorization")
        request.user = None
        try:
            token = authorization.replace("Bearer ", "")
            request.user = self._user_service.authorize(token)
        except:
            request.user = None
