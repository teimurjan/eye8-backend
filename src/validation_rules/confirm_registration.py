from src.validation_rules.validator import DataValidator

from typing import TypedDict


class ConfirmRegistrationData(TypedDict):
    token: str


class ConfirmRegistrationDataValidator(DataValidator[ConfirmRegistrationData]):
    def __init__(self):
        super().__init__(
            {"token": {"required": True, "nullable": False, "empty": False},}
        )
