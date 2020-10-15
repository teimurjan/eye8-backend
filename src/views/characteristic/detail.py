from src.validation_rules.characteristic.update import (
    UpdateCharacteristicData,
    UpdateCharacteristicDataValidator,
)
from src.utils.request import Request
from src.services.characteristic import CharacteristicService
from typing import Type
from src.serializers.characteristic import CharacteristicSerializer
from src.views.base import ValidatableView
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE


class CharacteristicDetailView(ValidatableView[UpdateCharacteristicData]):
    def __init__(
        self,
        validator: UpdateCharacteristicDataValidator,
        service: CharacteristicService,
        serializer_cls: Type[CharacteristicSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, characteristic_id: int):
        try:
            characteristic = self._service.get_one(characteristic_id)
            raw_intl = request.args.get("raw_intl") == "1"
            serialized_characteristic = (
                self._serializer_cls(characteristic)
                .in_language(None if raw_intl else request.language)
                .serialize()
            )
            return {"data": serialized_characteristic}, OK_CODE
        except self._service.CharacteristicNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, characteristic_id: int):
        try:
            valid_data = self._validate(request.get_json())
            characteristic = self._service.update(
                characteristic_id, valid_data, user=request.user
            )
            serialized_characteristic = self._serializer_cls(characteristic).serialize()
            return {"data": serialized_characteristic}, OK_CODE
        except self._service.CharacteristicNotFound:
            return {}, NOT_FOUND_CODE

    def delete(self, request: Request, characteristic_id: int):
        try:
            self._service.delete(characteristic_id, user=request.user)
            return {}, OK_CODE
        except self._service.CharacteristicNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, characteristic_id: int):
        try:
            self._service.get_one(characteristic_id)
            return {}, OK_CODE
        except self._service.CharacteristicNotFound:
            return {}, NOT_FOUND_CODE
