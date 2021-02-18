from src.utils.request import SideEffectType
from flask import jsonify, request, current_app as app
from flask.views import View

from src.constants.status_codes import (
    FORBIDDEN_CODE,
    METHOD_NOT_ALLOWED_CODE,
    UNAUTHORIZED_CODE,
    UNPROCESSABLE_ENTITY_CODE,
)
from src.errors import AccessRoleError, InvalidEntityFormat, NotAuthenticatedError


def get_cookie_domain():
    return (
        "." + app.config.get("HOST", "").replace("https://", "").replace("www.", ""),
    )


class AbstractView(View):
    def __init__(self, concrete_view, middlewares, on_respond_hooks=[]):
        self._concrete_view = concrete_view
        self._middlewares = middlewares
        self._on_respond_hooks = on_respond_hooks

    def dispatch_request(self, *args, **kwargs):
        try:
            self._apply_middlewares(request)

            handler = self._get_handler(request.method.lower())
            if handler is None:
                return None, METHOD_NOT_ALLOWED_CODE

            result = handler(request, **kwargs)
            body, status = result[0], result[1]

            response = jsonify(body or {})

            if len(result) > 2 and isinstance(result[2], dict):
                for name, value in result[2].items():
                    response.set_cookie(name, value, domain=get_cookie_domain(), httponly=True)

            self._handle_middleware_side_effects(request, response)
            self._handle_on_respond_hooks(request, body, status)

            return response, status

        except InvalidEntityFormat as e:
            errors = e.errors or {}
            return jsonify(errors), UNPROCESSABLE_ENTITY_CODE
        except AccessRoleError:
            return jsonify({}), FORBIDDEN_CODE
        except NotAuthenticatedError:
            return jsonify({}), UNAUTHORIZED_CODE

    def _apply_middlewares(self, request):
        for middleware in self._middlewares:
            middleware.handle(request)

    def _handle_middleware_side_effects(self, request, response):
        for side_effect in request.side_effects:
            if side_effect.type == SideEffectType.SetCookie:
                for name, cookie in side_effect.data.items():
                    response.set_cookie(
                        name,
                        cookie["value"],
                        domain=get_cookie_domain(),
                        httponly=cookie["httponly"],
                        expires=cookie["exp"],
                    )

    def _handle_on_respond_hooks(self, request, body, status):
        for hook in self._on_respond_hooks:
            hook(request, body, status)

    def _get_handler(self, http_method):
        if self._concrete_view is not None:
            return getattr(self._concrete_view, http_method)
        else:
            raise Exception("You must specify a view factory")
