from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.currency_rate import CurrencyRateSerializer
from src.services.currency_rate import CurrencyRateService
from src.views.base import ValidatableView


class CurrencyRateDetailView:
    def __init__(self, service: CurrencyRateService, serializer_cls: CurrencyRateSerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def delete(self, request, currency_rate_id):
        try:
            self._service.delete(currency_rate_id, user=request.user)
            return {}, OK_CODE
        except self._service.CurrencyRateNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CurrencyRateIsUntouchable:
            raise InvalidEntityFormat(
                {'orders': 'errors.hasOrdersWithThisRate'}
            )

    def head(self, request, currency_rate_id):
        try:
            self._service.get_one(currency_rate_id, user=request.user)
            return {}, OK_CODE
        except self._service.CurrencyRateNotFound:
            return {}, NOT_FOUND_CODE
