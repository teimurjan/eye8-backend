from src.validation_rules.validator import DataValidator

from typing import Dict, Optional, TypedDict


class CreateCategoryData(TypedDict):
    names: Dict[int, str]
    parent_category_id: Optional[int]


class CreateCategoryDataValidator(DataValidator[CreateCategoryData]):
    def __init__(self):
        super().__init__(
            {
                "names": {
                    "type": "dict",
                    "keyschema": {"regex": r"^[a-z]+$"},
                    "valueschema": {
                        "type": "string",
                        "required": True,
                        "empty": False,
                        "nullable": False,
                        "maxlength": 50,
                    },
                    "required": True,
                    "nullable": False,
                },
                "parent_category_id": {
                    "type": "integer",
                    "nullable": True,
                    "required": False,
                },
            }
        )
