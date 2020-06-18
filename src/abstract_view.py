from flask import jsonify, request
from flask.views import View

from src.constants.status_codes import (FORBIDDEN_CODE,
                                        METHOD_NOT_ALLOWED_CODE,
                                        UNAUTHORIZED_CODE,
                                        UNPROCESSABLE_ENTITY_CODE)
from src.errors import AccessRoleError, InvalidEntityFormat, NotAuthorizedError


class AbstractView(View):
    def __init__(self, concrete_view, middlewares, on_respond = None):
        self._concrete_view = concrete_view
        self._middlewares = middlewares
        self._on_respond = on_respond

    def dispatch_request(self, *args, **kwargs):
        try:
            self._handle_with_middlewares(request)

            handler = self._get_handler(request.method.lower())
            if handler is None:
                return None, METHOD_NOT_ALLOWED_CODE

            body, status = handler(request, **kwargs)
            if self._on_respond:
                self._on_respond(request, body, status)

            return jsonify(body or {}), status
        except InvalidEntityFormat as e:
            errors = e.errors or {}
            return jsonify(errors), UNPROCESSABLE_ENTITY_CODE
        except AccessRoleError:
            return jsonify({}), FORBIDDEN_CODE
        except NotAuthorizedError:
            return jsonify({}), UNAUTHORIZED_CODE

    def _handle_with_middlewares(self, request):
        for middleware in self._middlewares:
            middleware.handle(request)

    def _get_handler(self, http_method):
        if self._concrete_view is not None:
            return getattr(self._concrete_view, http_method)
        else:
            raise Exception('You must specify a view factory')
