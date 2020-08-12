import math

from src.errors import InvalidEntityFormat
from src.utils.number import parse_int


class ValidatableView:
    def __init__(self, validator):
        self._validator = validator

    def _validate(self, data):
        is_valid = self._validator.validate(data)
        if not is_valid:
            raise InvalidEntityFormat(self._validator.errors)


class PaginatableView:
    def _get_meta(self, count, page, limit):
        pages_count = math.ceil(count / limit)
        return {
            'count': count,
            'pages_count': pages_count,
            'page': page,
            'limit': limit,
        }

    def _get_pagination_data(self, request):
        page = parse_int(request.args.get('page'))
        if page:
            limit = parse_int(request.args.get('limit', 21))
            offset = limit * (page - 1)
            return {'page': page, 'offset': offset, 'limit': limit}
        return None
