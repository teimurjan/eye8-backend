from src.validation_rules.validator import DataValidator

from typing import TypedDict


class AuthenticationData(TypedDict):
    email: str
    password: str


class AuthenticationDataValidator(DataValidator[AuthenticationData]):
    def __init__(self):
        super().__init__(
            {
                "email": {"required": True, "empty": False, "nullable": False},
                "password": {"required": True, "empty": False, "nullable": False},
            }
        )
