import json
from typing import Dict, Optional, TypeVar

T = TypeVar("T")


def parse_json(s: str) -> T:
    try:
        return json.loads(s)
    except Exception:
        return None


def parse_json_from_form_data(form_data: Dict[str, Optional[str]], key="json") -> T:
    json_str = form_data.get(key)
    if json_str is None:
        return {}
    return parse_json(json_str) or {}
