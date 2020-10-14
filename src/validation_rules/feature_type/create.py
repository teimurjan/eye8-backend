from src.validation_rules.validator import DataValidator

from typing import Dict, TypedDict


class CreateFeatureTypeData(TypedDict):
    names: Dict[int, str]


class CreateFeatureTypeDataValidator(DataValidator[CreateFeatureTypeData]):
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
            }
        )
