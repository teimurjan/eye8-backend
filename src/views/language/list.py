from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.utils.number import parse_int


class LanguageListView:
    def __init__(self, service, serializer_cls):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        languages = self._service.get_all()

        serialized_languages = [
            self
            ._serializer_cls(language)
            .serialize()
            for language in languages
        ]

        return {'data': serialized_languages, 'meta': None}, OK_CODE
