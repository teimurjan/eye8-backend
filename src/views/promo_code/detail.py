from src.validation_rules.promo_code.update import (
    UpdatePromoCodeData,
    UpdatePromoCodeDataValidator,
)
from src.utils.request import Request
from typing import Type

from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService
from src.views.base import ValidatableView


class PromoCodeDetailView(ValidatableView[UpdatePromoCodeData]):
    def __init__(
        self,
        validator: UpdatePromoCodeDataValidator,
        service: PromoCodeService,
        serializer_cls: Type[PromoCodeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, promo_code_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            promo_code = self._service.get_one(promo_code_id, deleted=deleted)
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, promo_code_id: int):
        try:
            valid_data = self._validate(request.get_json())
            promo_code = self._service.update(
                promo_code_id, valid_data, user=request.user
            )
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.ValueNotUnique:
            raise InvalidEntityFormat({"value": "errors.alreadyExists"})

    def delete(self, request: Request, promo_code_id: int):
        try:
            forever = request.args.get("forever") == "1"

            if forever:
                self._service.delete_forever(promo_code_id, user=request.user)
            else:
                self._service.delete(promo_code_id, user=request.user)

            return {}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, promo_code_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            self._service.get_one(promo_code_id, deleted=deleted)
            return {}, OK_CODE
        except self._service.PromoCodeNotFound:
            return {}, NOT_FOUND_CODE
