from src.validation_rules.validator import DataValidator

from typing import List, Optional, TypedDict


class OrderItemData(TypedDict):
    product_id: int
    quantity: int
    product: Optional["product"]


class CreateOrderData(TypedDict):
    items: List[OrderItemData]
    feature_type_id: int
    user_name: str
    user_phone_number: str
    user_address: str
    promo_code: str


class CreateOrderDataValidator(DataValidator[CreateOrderData]):
    def __init__(self):
        super().__init__(
            {
                "items": {
                    "type": "list",
                    "schema": {
                        "product_id": {
                            "type": "integer",
                            "required": True,
                            "nullable": False,
                        },
                        "quantity": {
                            "type": "integer",
                            "required": True,
                            "nullable": False,
                        },
                    },
                    "required": True,
                    "nullable": False,
                },
                "user_name": {"type": "string", "required": True, "nullable": False},
                "user_phone_number": {
                    "type": "string",
                    "required": True,
                    "nullable": False,
                },
                "user_address": {"type": "string", "required": True, "nullable": False},
                "promo_code": {"type": "string", "required": False, "nullable": True},
            }
        )
