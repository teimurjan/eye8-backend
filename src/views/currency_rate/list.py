from src.validation_rules.currency_rate.create import (
    CreateCurrencyRateData,
    CreateCurrencyRateDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.constants.status_codes import OK_CODE, UNPROCESSABLE_ENTITY_CODE
from src.serializers.currency_rate import CurrencyRateSerializer
from src.services.currency_rate import CurrencyRateService
from src.views.base import ValidatableView


class CurrencyRateListView(ValidatableView[CreateCurrencyRateData]):
    def __init__(
        self,
        validator: CreateCurrencyRateDataValidator,
        service: CurrencyRateService,
        serializer_cls: Type[CurrencyRateSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        currency_rates = self._service.get_all()

        serialized_currency_rates = [
            self._serializer_cls(currency_rate).serialize()
            for currency_rate in currency_rates
        ]

        return {"data": serialized_currency_rates, "meta": None}, OK_CODE

    def post(self, request: Request):
        try:
            valid_data = self._validate(request.get_json())
            currency_rate = self._service.create(valid_data, user=request.user)
            serialized_currency_rate = self._serializer_cls(currency_rate).serialize()
            return {"data": serialized_currency_rate, "meta": None}, OK_CODE
        except self._service.AdditionLimitExceeded:
            return {"limit": "errors.limitExceeded"}, UNPROCESSABLE_ENTITY_CODE
