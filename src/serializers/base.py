from abc import abstractmethod

from sqlalchemy.orm.exc import DetachedInstanceError


class Serializer:
    def __init__(self):
        self._only_fields = None
        self._ignore_fields = None

    def _init_relation_safely(self, attr_name, obj, relation_name, default=None):
        setattr(self, attr_name, self._get_relation_safely(
            obj, relation_name, default))

    def _get_relation_safely(self, obj, relation_name, default=None):
        try:
            return getattr(obj, relation_name, default)
        except DetachedInstanceError:
            return default

    def only(self, only_fields):
        if only_fields:
            self._only_fields = only_fields
        return self

    def ignore(self, ignore_fields):
        if ignore_fields:
            self._ignore_fields = ignore_fields
        return self

    def _filter_fields(self, serialized_dict):
        filtered_dict = {}

        for field in serialized_dict.keys():
            is_field_in_only = not self._only_fields or field in self._only_fields
            is_field_in_ignore = self._ignore_fields and field in self._ignore_fields
            if is_field_in_only and not is_field_in_ignore:
                filtered_dict[field] = serialized_dict[field]

        return filtered_dict

    def _with_serialized_relation(self, attr_name, model_cls, serializer_cls, before_serialize=None):
        if isinstance(getattr(self, attr_name), model_cls):
            serializer = serializer_cls(getattr(self, attr_name))

            if before_serialize is not None and callable(before_serialize):
                before_serialize(serializer)

            setattr(
                self,
                attr_name,
                serializer.serialize()
            )
        return self

    def _serialize_relation(self, attr_name, model_cls):
        if isinstance(getattr(self, attr_name), model_cls):
            return getattr(self, attr_name).id
        return getattr(self, attr_name)

    def _with_serialized_relations(self, attr_name, model_cls, serializer_cls, before_serialize=None):
        attr = getattr(self, attr_name)
        if attr is None:
            return self

        serialized = []
        for model in attr:
            serializer = serializer_cls(model)

            if before_serialize is not None and callable(before_serialize):
                before_serialize(serializer)

            serialized.append(serializer.serialize())

        setattr(self, attr_name, serialized)
        return self

    def _serialize_relations(self, attr_name, model_cls):
        if getattr(self, attr_name) and isinstance(getattr(self, attr_name)[0], model_cls):
            return [i.id for i in getattr(self, attr_name)]
        return getattr(self, attr_name)

    def chain(self, fn):
        fn(self)

        return self

    @abstractmethod
    def serialize(self):
        raise NotImplementedError()
