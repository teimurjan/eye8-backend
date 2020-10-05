from src.validation_rules.characteristic.create import (
    CreateCharacteristicData,
    CreateCharacteristicDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.serializers.characteristic import CharacteristicSerializer
from src.constants.status_codes import OK_CODE
from src.services.characteristic import CharacteristicService
from src.views.base import PaginatableView, ValidatableView


class CharacteristicListView(ValidatableView[CreateCharacteristicData], PaginatableView):
    def __init__(
        self,
        validator: CreateCharacteristicDataValidator,
        service: CharacteristicService,
        serializer_cls: Type[CharacteristicSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        pagination_data = self._get_pagination_data(request)

        meta = None
        characteristics = []

        if pagination_data:
            characteristics, count = self._service.get_all(
                offset=pagination_data["offset"], limit=pagination_data["limit"]
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            characteristics, _ = self._service.get_all()

        should_get_raw_intl_field = request.args.get("raw_intl") == "1"
        serialized_characteristics = [
            self._serializer_cls(characteristic)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for characteristic in characteristics
        ]
        return {"data": serialized_characteristics, "meta": meta}, OK_CODE

    def post(self, request: Request):
        valid_data = self._validate(request.get_json())
        characteristic = self._service.create(valid_data, user=request.user)
        serialized_characteristic = self._serializer_cls(characteristic).serialize()
        return {"data": serialized_characteristic}, OK_CODE
