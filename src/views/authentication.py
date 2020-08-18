from src.validation_rules.authentication import (
    AuthenticationData,
    AuthenticationDataValidator,
)
from src.utils.request import Request


from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.user import UserService
from src.views.base import ValidatableView


class AuthenticationView(ValidatableView[AuthenticationData]):
    def __init__(
        self, user_service: UserService, validator: AuthenticationDataValidator
    ):
        super().__init__(validator)
        self._user_service = user_service

    def post(self, request: Request):
        try:
            valid_data = self._validate(request.get_json())
            access_token, refresh_token = self._user_service.authenticate(valid_data)
            return (
                {"access_token": access_token, "refresh_token": refresh_token},
                OK_CODE,
            )
        except self._user_service.AuthCredsInvalid:
            raise InvalidEntityFormat(
                {"credentials": "errors.emailOrPasswordIncorrect"}
            )
