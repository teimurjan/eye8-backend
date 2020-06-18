import json


def parse_json(s):
    try:
        return json.loads(s)
    except Exception:
        return None


def parse_json_from_form_data(form_data, key='json'):
    json_str = form_data.get(key)
    if json_str is None:
        return {}
    return parse_json(json_str) or {}
