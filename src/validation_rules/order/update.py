from src.validation_rules.order.create import OrderItemData
from src.models.order import OrderStatus
from src.validation_rules.validator import DataValidator

from typing import List, TypedDict


class UpdateOrderData(TypedDict):
    items: List[OrderItemData]
    feature_type_id: int
    user_name: str
    user_phone_number: str
    user_address: str
    status: OrderStatus
    promo_code: str


class UpdateOrderDataValidator(DataValidator[UpdateOrderData]):
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
                "status": {
                    "type": "string",
                    "allowed": ['idle', 'completed', 'approved', 'rejected'],
                    "required": True,
                    "nullable": False,
                },
                "promo_code": {"type": "string", "required": False, "nullable": True},
            }
        )
