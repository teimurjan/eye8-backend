import math
from src.validation_rules.validator import DataValidator
from typing import Dict, TypeVar, Generic

from src.utils.request import Request


from src.errors import InvalidEntityFormat
from src.utils.number import parse_int

V = TypeVar("V")


class ValidatableView(Generic[V]):
    def __init__(self, validator: DataValidator[V]):
        self._validator = validator

    def _validate(self, data: Dict) -> V:
        try:
            return self._validator.validate(data)
        except self._validator.ValidationError as e:
            raise InvalidEntityFormat(e.errors)


class PaginatableView:
    def _get_meta(self, count: int, page: int, limit: int):
        pages_count = math.ceil(count / limit)
        return {
            "count": count,
            "pages_count": pages_count,
            "page": page,
            "limit": limit,
        }

    def _get_pagination_data(self, request: Request):
        page = parse_int(request.args.get("page"))
        if page:
            limit = parse_int(request.args.get("limit", 21))
            offset = limit * (page - 1)
            return {"page": page, "offset": offset, "limit": limit}
        return None
