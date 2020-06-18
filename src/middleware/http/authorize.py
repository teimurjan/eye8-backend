from src.constants.headers import AUTHORIZATION_HEADER


class AuthorizeHttpMiddleware:
    def __init__(self, user_service):
        self._user_service = user_service

    def handle(self, request):
        authorization = request.headers.get('Authorization')
        request.user = None
        if authorization is not None:
            token = authorization.replace('Bearer ', '')
            request.user = self._user_service.authorize(token)
