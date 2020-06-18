from cerberus.validator import Validator

from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.signup import SignupService
from src.views.base import ValidatableView


class RegistrationView(ValidatableView):
    def __init__(self, signup_service: SignupService, validator: Validator):
        super().__init__(validator)
        self._signup_service = signup_service

    def post(self, request):
        try:
            data = request.get_json()
            self._validate(data)

            self._signup_service.create_and_send(data, request.language)

            return {}, OK_CODE
        except self._signup_service.SameEmail:
            raise InvalidEntityFormat({'email': 'errors.same'})
