from typing import TypeVar


T = TypeVar('T')


def parse_int(s: T):
    try:
        return int(s)
    except Exception:
        return None
