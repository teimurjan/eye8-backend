from typing import Type

from cerberus.validator import Validator

from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.promo_code import PromoCodeSerializer
from src.services.promo_code import PromoCodeService
from src.utils.request import Request
from src.views.base import ValidatableView


class PromoCodeListView(ValidatableView):
    def __init__(
        self,
        validator: Validator,
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
            data = request.get_json()
            self._validate(data)
            promo_code = self._service.create(data, user=request.user)
            serialized_promo_code = (
                self._serializer_cls(promo_code)
                .in_language(request.language)
                .serialize()
            )
            return {"data": serialized_promo_code}, OK_CODE
        except self._service.ValueNotUnique:
            raise InvalidEntityFormat({"value": "errors.alreadyExists"})
