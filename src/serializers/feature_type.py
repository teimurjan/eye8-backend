from src.serializers.intl import IntlSerializer


class FeatureTypeSerializer(IntlSerializer):
    def __init__(self, feature_type):
        super().__init__()
        self._id = feature_type.id
        self._name_en = feature_type.name_en
        self._name_ru = feature_type.name_ru
        self._created_on = feature_type.created_on
        self._updated_on = feature_type.updated_on

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "name": self._get_intl_field_from("name", self),
                "created_on": self._created_on,
                "updated_on": self._updated_on,
            }
        )
