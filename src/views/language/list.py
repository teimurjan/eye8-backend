from src.services.language import LanguageService
from src.serializers.language import LanguageSerializer
from typing import Type
from src.constants.status_codes import OK_CODE


class LanguageListView:
    def __init__(
        self, service: LanguageService, serializer_cls: Type[LanguageSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        languages = self._service.get_all()

        serialized_languages = [
            self._serializer_cls(language).serialize() for language in languages
        ]

        return {"data": serialized_languages, "meta": None}, OK_CODE
