from src.validation_rules.validator import DataValidator

from typing import Dict, TypedDict


class CreateFeatureValueData(TypedDict):
    names: Dict[int, str]
    feature_type_id: int


class CreateFeatureValueDataValidator(DataValidator[CreateFeatureValueData]):
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
                "feature_type_id": {
                    "type": "integer",
                    "nullable": False,
                    "required": True,
                },
            }
        )
