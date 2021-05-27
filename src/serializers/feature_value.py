from src.models.feature_type import FeatureType
from src.serializers.intl import IntlSerializer
from src.serializers.feature_type import FeatureTypeSerializer


class FeatureValueSerializer(IntlSerializer):
    def __init__(self, feature_value):
        super().__init__()
        self._id = feature_value.id
        self._name_en = feature_value.name_en
        self._name_ru = feature_value.name_ru
        self._feature_type = feature_value.feature_type
        self._created_on = feature_value.created_on
        self._updated_on = feature_value.updated_on

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "name": self._get_intl_field_from("name", self),
                "feature_type": self._serialize_feature_type(),
                "created_on": self._created_on,
                "updated_on": self._updated_on,
            }
        )

    def with_serialized_feature_type(self):
        self._with_serialized_relation(
            "_feature_type",
            FeatureType,
            FeatureTypeSerializer,
            lambda serializer: serializer.in_language(self._language),
        )
        return self

    def _serialize_feature_type(self):
        return self._serialize_relation("_feature_type", FeatureType)
