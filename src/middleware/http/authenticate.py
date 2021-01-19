from src.utils.request import Request, SideEffect, SideEffectType
from src.services.user import UserService
import datetime


def get_logout_side_effect():
    return SideEffect(
        SideEffectType.SetCookie,
        {
            "access_token": {"value": "", "httponly": False, "exp": 0,},
            "refresh_token": {"value": "", "httponly": True, "exp": 0,},
        },
    )


def get_refresh_side_effect(access_token: str, refresh_token: str):
    expire_date = datetime.datetime.now() + datetime.timedelta(days=7)

    return SideEffect(
        SideEffectType.SetCookie,
        {
            "access_token": {
                "value": access_token,
                "httponly": False,
                "exp": expire_date,
            },
            "refresh_token": {
                "value": refresh_token,
                "httponly": True,
                "exp": expire_date,
            },
        },
    )


class AuthenticateHttpMiddleware:
    def __init__(self, user_service: UserService):
        self._user_service = user_service

    def handle(self, request: Request):
        authorization = request.headers.get("Authorization")
        request.user = None
        try:
            token = authorization.replace("Bearer ", "")
            if token == "loggedout":
                request.side_effects.append(get_logout_side_effect())
                return
            request.user = self._user_service.authorize(token)
        except:
            self._attempt_refresh(request)

    def _attempt_refresh(self, request: Request):
        old_refresh_token = request.cookies.get("refresh_token")
        if old_refresh_token:
            try:
                access_token, refresh_token = self._user_service.refresh_token(
                    old_refresh_token
                )

                request.user = self._user_service.authorize(access_token)

                request.side_effects.append(
                    get_refresh_side_effect(access_token, refresh_token)
                )
            except:
                request.user = None
        request.user = None

