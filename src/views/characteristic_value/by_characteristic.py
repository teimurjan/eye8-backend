from src.utils.request import Request
from typing import Type
from src.constants.status_codes import OK_CODE
from src.serializers.characteristic_value import CharacteristicValueSerializer
from src.services.characteristic_value import CharacteristicValueService


class CharacteristicValueByCharacteristicView:
    def __init__(
        self,
        service: CharacteristicValueService,
        serializer_cls: Type[CharacteristicValueSerializer],
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, characteristic_id: int):
        raw_intl = request.args.get("raw_intl") == "1"
        characteristic_values = []

        characteristic_values = self._service.get_all_by_characteristic(
            characteristic_id
        )

        serialized_characteristic_values = [
            self._serializer_cls(characteristic)
            .in_language(None if raw_intl else request.language)
            .serialize()
            for characteristic in characteristic_values
        ]

        return {"data": serialized_characteristic_values}, OK_CODE
