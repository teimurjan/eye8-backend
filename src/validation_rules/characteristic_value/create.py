from src.validation_rules.validator import DataValidator

from typing import Dict, TypedDict


class CreateCharacteristicValueData(TypedDict):
    names: Dict[int, str]
    characteristic_id: int


class CreateCharacteristicValueDataValidator(DataValidator[CreateCharacteristicValueData]):
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
                "characteristic_id": {
                    "type": "integer",
                    "nullable": False,
                    "required": True,
                },
            }
        )
