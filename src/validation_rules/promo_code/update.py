from src.validation_rules.validator import DataValidator

from typing import List, Optional, TypedDict


class UpdatePromoCodeData(TypedDict):
    value: str
    is_active: Optional[bool]
    disable_on_use: Optional[bool]
    products_ids: List[int]


class UpdatePromoCodeDataValidator(DataValidator[UpdatePromoCodeData]):
    def __init__(self):
        super().__init__(
            {
                "is_active": {"type": "boolean", "required": True, "nullable": False},
                "disable_on_use": {
                    "type": "boolean",
                    "required": True,
                    "nullable": False,
                },
                "products_ids": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
            }
        )
