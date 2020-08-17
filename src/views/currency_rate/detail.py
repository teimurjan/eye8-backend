from typing import Type
from src.utils.request import Request
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.currency_rate import CurrencyRateSerializer
from src.services.currency_rate import CurrencyRateService


class CurrencyRateDetailView:
    def __init__(
        self, service: CurrencyRateService, serializer_cls: Type[CurrencyRateSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def delete(self, request: Request, currency_rate_id: int):
        try:
            self._service.delete(currency_rate_id, user=request.user)
            return {}, OK_CODE
        except self._service.CurrencyRateNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CurrencyRateIsUntouchable:
            raise InvalidEntityFormat({"orders": "errors.hasOrdersWithThisRate"})

    def head(self, request: Request, currency_rate_id: int):
        try:
            self._service.get_one(currency_rate_id, user=request.user)
            return {}, OK_CODE
        except self._service.CurrencyRateNotFound:
            return {}, NOT_FOUND_CODE
