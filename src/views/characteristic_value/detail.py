from src.validation_rules.characteristic_value.update import (
    UpdateCharacteristicValueDataValidator,
    UpdateCharacteristicValueData,
)
from src.utils.request import Request
from src.services.characteristic_value import CharacteristicValueService
from src.serializers.characteristic_value import CharacteristicValueSerializer
from typing import Type

from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE


class CharacteristicValueDetailView(ValidatableView[UpdateCharacteristicValueData]):
    def __init__(
        self,
        validator: UpdateCharacteristicValueDataValidator,
        service: CharacteristicValueService,
        serializer_cls: Type[CharacteristicValueSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, characteristic_value_id: int):
        try:
            characteristic_value = self._service.get_one(characteristic_value_id)
            raw_intl = request.args.get("raw_intl") == "1"
            serialized_characteristic_value = (
                self._serializer_cls(characteristic_value)
                .in_language(None if raw_intl else request.language)
                .with_serialized_characteristic()
                .serialize()
            )
            return {"data": serialized_characteristic_value}, OK_CODE
        except self._service.CharacteristicValueNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, characteristic_value_id: int):
        try:
            valid_data = self._validate(request.get_json())
            characteristic_value = self._service.update(
                characteristic_value_id, valid_data, user=request.user
            )
            serialized_characteristic_value = (
                self._serializer_cls(characteristic_value)
                .with_serialized_characteristic()
                .serialize()
            )
            return {"data": serialized_characteristic_value}, OK_CODE
        except self._service.CharacteristicValueNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CharacteristicInvalid:
            raise InvalidEntityFormat({"characteristic": "errors.invalidID"})

    def delete(self, request: Request, characteristic_value_id: int):
        try:
            self._service.delete(characteristic_value_id, user=request.user)
            return {}, OK_CODE
        except self._service.CharacteristicValueNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, characteristic_value_id: int):
        try:
            self._service.get_one(characteristic_value_id)
            return {}, OK_CODE
        except self._service.CharacteristicValueNotFound:
            return {}, NOT_FOUND_CODE
