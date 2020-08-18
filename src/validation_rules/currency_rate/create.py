from src.validation_rules.validator import DataValidator

from typing import TypedDict, Union


class CreateCurrencyRateData(TypedDict):
    name: str
    value: Union[int, float]


class CreateCurrencyRateDataValidator(DataValidator[CreateCurrencyRateData]):
    def __init__(self):
        super().__init__(
            {
                "name": {"type": "string", "required": True, "nullable": True},
                "value": {"type": "number", "required": True, "nullable": False},
            }
        )
