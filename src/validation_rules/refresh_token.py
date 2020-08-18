from src.validation_rules.validator import DataValidator

from typing import TypedDict


class RefreshTokenData(TypedDict):
    refresh_token: str


class RefreshTokenDataValidator(DataValidator[RefreshTokenData]):
    def __init__(self):
        super().__init__(
            {"refresh_token": {"required": True, "nullable": False, "empty": False},}
        )
