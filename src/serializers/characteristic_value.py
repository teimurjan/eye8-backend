from src.serializers.intl import IntlSerializer
from src.serializers.characteristic import CharacteristicSerializer
from src.models.characteristic import Characteristic


class CharacteristicValueSerializer(IntlSerializer):
    def __init__(self, characteristic_value):
        super().__init__()
        self._id = characteristic_value.id
        self._name_en = characteristic_value.name_en
        self._name_ru = characteristic_value.name_ru
        self._characteristic = characteristic_value.characteristic
        self._created_on = characteristic_value.created_on
        self._updated_on = characteristic_value.updated_on

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "name": self._get_intl_field_from("name", self),
                "characteristic": self._serialize_characteristic(),
                "created_on": self._created_on,
                "updated_on": self._updated_on,
            }
        )

    def with_serialized_characteristic(self):
        self._with_serialized_relation(
            "_characteristic",
            Characteristic,
            CharacteristicSerializer,
            lambda serializer: serializer.in_language(self._language),
        )
        return self

    def _serialize_characteristic(self):
        return self._serialize_relation("_characteristic", Characteristic)
