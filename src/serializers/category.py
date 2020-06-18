from src.serializers.intl import IntlSerializer


class CategorySerializer(IntlSerializer):
    def __init__(self, category):
        super().__init__()
        self._id = category.id
        self._names = category.names
        self._parent_category_id = category.parent_category_id
        self._slug = category.slug
        self._created_on = category.created_on
        self._updated_on = category.updated_on

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'name': self._serialize_name(),
            'parent_category_id': self._parent_category_id,
            'slug': self._slug,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
        })

    def _serialize_name(self):
        return self._get_intl_field_from(self._names)
