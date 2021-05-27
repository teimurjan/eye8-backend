from abc import abstractmethod
from typing import Optional, TypeVar

from src.serializers.base import Serializer

T = TypeVar("T")


class IntlSerializer(Serializer):
    def __init__(self):
        super().__init__()
        self._language: Optional[str] = None

    def in_language(self, language: Optional[str]):
        if language:
            self._language = language
        return self

    def _get_intl_field_from(self, key: str, obj: T):
        if self._language is None:
            return {"en": getattr(obj, f"_{key}_en"), "ru": getattr(obj, f"_{key}_ru")}

        return getattr(obj, f"_{key}_{self._language}")

    @abstractmethod
    def serialize(self) -> str:
        raise NotImplementedError()
