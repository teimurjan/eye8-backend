from src.serializers.base import Serializer


class GroupSerializer(Serializer):
    def __init__(self, group):
        super().__init__()
        self._id = group.id
        self._name = group.name,
        self._created_on = group.created_on
        self._updated_on = group.updated_on

    def serialize(self):
        return self._filter_fields({
            'name': self._name,
            'id': self._id,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
        })
