from src.serializers.intl import IntlSerializer


class CharacteristicSerializer(IntlSerializer):
    def __init__(self, characteristic):
        super().__init__()
        self._id = characteristic.id
        self._name_en = characteristic.name_en
        self._name_ru = characteristic.name_ru
        self._created_on = characteristic.created_on
        self._updated_on = characteristic.updated_on

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "name": self._get_intl_field_from("name", self),
                "created_on": self._created_on,
                "updated_on": self._updated_on,
            }
        )

