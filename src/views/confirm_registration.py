from src.utils.request import Request
from cerberus.validator import Validator

from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.services.signup import SignupService
from src.views.base import ValidatableView


class ConfirmRegistrationView(ValidatableView):
    def __init__(self, signup_service: SignupService, validator: Validator):
        super().__init__(validator)
        self._signup_service = signup_service

    def post(self, request: Request):
        try:
            data = request.get_json()
            self._validate(data)

            self._signup_service.confirm(data["token"])

            return {}, OK_CODE
        except self._signup_service.SignupNotFound:
            return {}, NOT_FOUND_CODE
