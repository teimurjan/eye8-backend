from src.models.intl import Language
from src.serializers.base import Serializer


class CurrencyRateSerializer(Serializer):
    def __init__(self, currency_rate):
        super().__init__()
        self._id = currency_rate.id
        self._name = currency_rate.name
        self._value = currency_rate.value
        self._created_on = currency_rate.created_on
        self._updated_on = currency_rate.updated_on

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'name': self._name,
            'value': self._value,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
        })
