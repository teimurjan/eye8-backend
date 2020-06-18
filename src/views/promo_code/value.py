from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService
from src.views.base import ValidatableView


class PromoCodeValueView:
    def __init__(self, service: PromoCodeService, serializer_cls: PromoCodeSerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, value):
        try:
            promo_code = self._service.get_one_by_value(value.lower())
            serialized_promo_code = (
                self
                ._serializer_cls(promo_code)
                .in_language(request.language)
                .add_products(promo_code.products)
                .serialize()
            )
            return {'data': serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
