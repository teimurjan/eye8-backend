from src.constants.status_codes import OK_CODE
from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
import json


class AuthenticationView(ValidatableView):
    def __init__(self, user_service, validator):
        super().__init__(validator)
        self._user_service = user_service

    def post(self, request):
        try:
            data = request.get_json()
            self._validate(data)
            access_token, refresh_token = self._user_service.authenticate(data)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, OK_CODE
        except self._user_service.AuthCredsInvalid:
            raise InvalidEntityFormat({
                'credentials': 'errors.emailOrPasswordIncorrect'
            })
