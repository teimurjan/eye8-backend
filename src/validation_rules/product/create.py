from src.validation_rules.validator import DataValidator

from typing import List, Optional, TypedDict


class CreateProductData(TypedDict):
    product_type_id: int
    images: List[str]
    price: int
    discount: Optional[int]
    quantity: int
    feature_values: List[int]


class CreateProductDataValidator(DataValidator[CreateProductData]):
    def __init__(self):
        super().__init__(
            {
                "product_type_id": {
                    "type": "integer",
                    "required": True,
                    "nullable": False,
                },
                "images": {
                    "type": "list",
                    "schema": {"required": True, "nullable": False},
                    "required": True,
                    "nullable": False,
                    "minlength": 0,
                    "maxlength": 4,
                },
                "price": {
                    "type": "integer",
                    "required": True,
                    "min": 1,
                    "nullable": False,
                },
                "discount": {
                    "type": "integer",
                    "required": True,
                    "min": -1,
                    "max": 100,
                    "nullable": True,
                },
                "quantity": {
                    "type": "integer",
                    "required": True,
                    "min": 0,
                    "nullable": False,
                },
                "feature_values": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
            }
        )
