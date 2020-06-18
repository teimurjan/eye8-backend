from abc import abstractmethod

from src.serializers.base import Serializer


class IntlSerializer(Serializer):
    def __init__(self):
        super().__init__()
        self._language = None

    def in_language(self, language):
        if language:
            self._language = language
        return self

    def _get_intl_field_from(self, all_fields):
        if self._language is None:
            return {field.language_id: field.value for field in all_fields}

        values = [
            field.value for field in all_fields if field.language_id == self._language.id
        ]
        return "" if len(values) == 0 else values[0]

    @abstractmethod
    def serialize(self):
        raise NotImplementedError()
