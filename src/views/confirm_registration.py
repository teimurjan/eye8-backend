from src.validation_rules.confirm_registration import (
    ConfirmRegistrationData,
    ConfirmRegistrationDataValidator,
)
from src.utils.request import Request

from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.services.signup import SignupService
from src.views.base import ValidatableView


class ConfirmRegistrationView(ValidatableView[ConfirmRegistrationData]):
    def __init__(
        self, signup_service: SignupService, validator: ConfirmRegistrationDataValidator
    ):
        super().__init__(validator)
        self._signup_service = signup_service

    def post(self, request: Request):
        try:
            valid_data = self._validate(request.get_json())
            self._signup_service.confirm(valid_data["token"])
            return {}, OK_CODE
        except self._signup_service.SignupNotFound:
            return {}, NOT_FOUND_CODE
