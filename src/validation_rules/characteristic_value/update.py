from src.validation_rules.validator import DataValidator

from typing import Dict, TypedDict


class UpdateCharacteristicValueData(TypedDict):
    names: Dict[int, str]
    characteristic_id: int


class UpdateCharacteristicValueDataValidator(
    DataValidator[UpdateCharacteristicValueData]
):
    def __init__(self):
        super().__init__(
            {
                "names": {
                    "type": "dict",
                    "keyschema": {"regex": r"^\d+$"},
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
