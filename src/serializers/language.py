from src.models.intl import Language
from src.serializers.base import Serializer


class LanguageSerializer(Serializer):
    def __init__(self, language):
        super().__init__()
        self._id = language.id
        self._name = language.name
        self._created_on = language.created_on
        self._updated_on = language.updated_on

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'name': self._name,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
        })
