from src.validation_rules.validator import DataValidator

from typing import Dict, TypedDict


class UpdateCharacteristicData(TypedDict):
    names: Dict[int, str]


class UpdateCharacteristicDataValidator(DataValidator[UpdateCharacteristicData]):
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
            }
        )
