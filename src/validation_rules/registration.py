from src.validation_rules.utils import EMAIL_REGEX, PASSWORD_REGEX
from src.validation_rules.validator import DataValidator

from typing import TypedDict


class RegistrationData(TypedDict):
    name: str
    email: str
    password: str


class RegistrationDataValidator(DataValidator[RegistrationData]):
    def __init__(self):
        super().__init__(
            {
                "name": {"required": True, "nullable": False, "empty": False},
                "email": {"required": True, "nullable": False, "regex": EMAIL_REGEX},
                "password": {
                    "required": True,
                    "nullable": False,
                    "regex": PASSWORD_REGEX,
                },
            }
        )
