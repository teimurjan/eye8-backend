from src.validation_rules.validator import DataValidator

from typing import List, Optional, TypedDict


class CreatePromoCodeData(TypedDict):
    discount: int
    amount: Optional[int]
    value: str
    is_active: Optional[bool]
    disable_on_use: Optional[bool]
    products: List[int]


class CreatePromoCodeDataValidator(DataValidator[CreatePromoCodeData]):
    def __init__(self):
        super().__init__(
            {
                "discount": {
                    "type": "integer",
                    "required": True,
                    "min": -1,
                    "max": 100,
                    "nullable": False,
                },
                "amount": {"type": "number", "required": False, "nullable": True},
                "value": {
                    "type": "string",
                    "required": True,
                    "nullable": False,
                    "maxlength": 60,
                },
                "is_active": {"type": "boolean", "required": False, "nullable": False},
                "disable_on_use": {
                    "type": "boolean",
                    "required": False,
                    "nullable": False,
                },
                "products": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
            }
        )
