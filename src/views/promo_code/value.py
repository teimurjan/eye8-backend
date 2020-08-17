from src.utils.request import Request
from typing import Type
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService


class PromoCodeValueView:
    def __init__(
        self, service: PromoCodeService, serializer_cls: Type[PromoCodeSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, value: str):
        try:
            promo_code = self._service.get_one_by_value(value.lower())
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .with_serialized_products()
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
