from src.validation_rules.validator import DataValidator

from typing import Dict, Optional, TypedDict


class CreateBannerData(TypedDict):
    texts: Dict[int, str]
    image: str
    link: Optional[str]
    text_color: Optional[str]
    link_texts: Dict[int, str]
    text_top_offset: Optional[int]
    text_bottom_offset: Optional[int]
    text_left_offset: Optional[int]
    text_right_offset: Optional[int]


class CreateBannerDataValidator(DataValidator[CreateBannerData]):
    def __init__(self):
        super().__init__(
            {
                "texts": {
                    "type": "dict",
                    "keyschema": {"regex": r"^[a-z]+$"},
                    "valueschema": {
                        "type": "string",
                        "required": True,
                        "empty": False,
                        "nullable": False,
                    },
                    "required": True,
                    "nullable": False,
                },
                "image": {"required": True, "nullable": False},
                "link": {"required": False, "nullable": True},
                "text_color": {"required": False, "nullable": True},
                "link_texts": {
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
                "text_top_offset": {
                    "type": "integer",
                    "required": False,
                    "nullable": True,
                },
                "text_bottom_offset": {
                    "type": "integer",
                    "required": False,
                    "nullable": True,
                },
                "text_left_offset": {
                    "type": "integer",
                    "required": False,
                    "nullable": True,
                },
                "text_right_offset": {
                    "type": "integer",
                    "required": False,
                    "nullable": True,
                },
            },
        )
