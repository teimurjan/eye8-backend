from src.utils.request import Request
from typing import Type

from cerberus.validator import Validator

from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService
from src.views.base import ValidatableView


class PromoCodeDetailView(ValidatableView):
    def __init__(
        self,
        validator: Validator,
        service: PromoCodeService,
        serializer_cls: Type[PromoCodeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, promo_code_id: int):
        try:
            promo_code = self._service.get_one(promo_code_id)
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .with_serialized_products()
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request, promo_code_id: int):
        try:
            data = request.get_json()
            self._validate(data)
            promo_code = self._service.update(promo_code_id, data, user=request.user)
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.PromoCodeWithOrdersIsUntouchable:
            raise InvalidEntityFormat({"orders": "errors.hasOrders"})
        except self._service.ValueNotUnique:
            raise InvalidEntityFormat({"value": "errors.alreadyExists"})

    def delete(self, request: Request, promo_code_id: int):
        try:
            self._service.delete(promo_code_id, user=request.user)
            return {}, OK_CODE
        except self._service.PromoCodeWithOrdersIsUntouchable:
            raise InvalidEntityFormat({"orders": "errors.hasOrders"})
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, promo_code_id: int):
        try:
            self._service.get_one(promo_code_id)
            return {}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
