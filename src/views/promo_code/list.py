from src.validation_rules.promo_code.create import (
    CreatePromoCodeData,
    CreatePromoCodeDataValidator,
)
from typing import Type

from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService
from src.utils.request import Request
from src.views.base import ValidatableView


class PromoCodeListView(ValidatableView[CreatePromoCodeData]):
    def __init__(
        self,
        validator: CreatePromoCodeDataValidator,
        service: PromoCodeService,
        serializer_cls: Type[PromoCodeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        deleted = request.args.get("deleted") == "1"
        promo_codes, _ = self._service.get_all(deleted=deleted, user=request.user)

        serialized_promo_codes = [
            self._serializer_cls(promo_code).in_language(request.language).serialize()
            for promo_code in promo_codes
        ]
        return {"data": serialized_promo_codes}, OK_CODE

    def post(self, request: Request):
        try:
            valid_data = self._validate(request.get_json())
            promo_code = self._service.create(valid_data, user=request.user)
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.ValueNotUnique:
            raise InvalidEntityFormat({"value": "errors.alreadyExists"})
