from src.validation_rules.characteristic_value.create import (
    CreateCharacteristicValueData,
    CreateCharacteristicValueDataValidator,
)
from typing import Type
from src.serializers.characteristic_value import CharacteristicValueSerializer
from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.characteristic_value import CharacteristicValueService
from src.views.base import PaginatableView, ValidatableView


class CharacteristicValueListView(
    ValidatableView[CreateCharacteristicValueData], PaginatableView
):
    def __init__(
        self,
        validator: CreateCharacteristicValueDataValidator,
        service: CharacteristicValueService,
        serializer_cls: Type[CharacteristicValueSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        pagination_data = self._get_pagination_data(request)

        meta = None
        characteristic_values = []

        if pagination_data:
            characteristic_values, count = self._service.get_all(
                offset=pagination_data["offset"], limit=pagination_data["limit"]
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            characteristic_values, _ = self._service.get_all()

        raw_intl = request.args.get("raw_intl") == "1"

        serialized_characteristic_values = [
            self._serializer_cls(characteristic_value)
            .in_language(None if raw_intl else request.language)
            .with_serialized_characteristic()
            .serialize()
            for characteristic_value in characteristic_values
        ]
        return {"data": serialized_characteristic_values, "meta": meta}, OK_CODE

    def post(self, request):
        try:
            valid_data = self._validate(request.get_json())
            characteristic_value = self._service.create(valid_data, user=request.user)
            serialized_characteristic_value = (
                self._serializer_cls(characteristic_value)
                .with_serialized_characteristic()
                .serialize()
            )
            return {"data": serialized_characteristic_value}, OK_CODE
        except self._service.CharacteristicInvalid:
            raise InvalidEntityFormat({"characteristic_id": "errors.invalidID"})
