from typing import Callable, List, Optional, TypeVar


T = TypeVar("T")


def find_in_array(arr: List[T], cb: Callable[[T], bool]) -> Optional[T]:
    for i, el in enumerate(arr):
        if cb(el):
            return i, el

    return -1, None
