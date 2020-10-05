from src.validation_rules.validator import DataValidator

from typing import Dict, List, TypedDict


class UpdateProductTypeData(TypedDict):
    names: Dict[int, str]
    descriptions: Dict[int, str]
    short_descriptions: Dict[int, str]
    feature_types: List[int]
    characteristic_values: List[int]
    categories: List[int]
    instagram_links: List[str]
    image: str


class UpdateProductTypeDataValidator(DataValidator[UpdateProductTypeData]):
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
                "descriptions": {
                    "type": "dict",
                    "keyschema": {"regex": r"^\d+$"},
                    "valueschema": {
                        "type": "string",
                        "required": True,
                        "empty": False,
                        "nullable": False,
                    },
                    "required": True,
                    "nullable": False,
                },
                "short_descriptions": {
                    "type": "dict",
                    "keyschema": {"regex": r"^\d+$"},
                    "valueschema": {
                        "type": "string",
                        "required": True,
                        "empty": False,
                        "nullable": False,
                        "maxlength": 1000,
                    },
                    "required": True,
                    "nullable": False,
                },
                "feature_types": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
                "characteristic_values": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
                "instagram_links": {
                    "type": "list",
                    "schema": {
                        "type": "string",
                        "nullable": False,
                        "regex": r"(https?:\/\/(?:www\.)?instagram\.com\/p\/([^/?#&]+)).*",
                    },
                    "required": True,
                    "nullable": False,
                },
                "categories": {
                    "type": "list",
                    "schema": {"type": "integer", "nullable": False},
                    "required": True,
                    "nullable": False,
                },
                "image": {"required": True, "nullable": False},
            }
        )
