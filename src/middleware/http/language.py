from src.constants.headers import ACCEPT_LANGUAGE_HEADER
from src.repos.language import LanguageRepo


class LanguageHttpMiddleware:
    def __init__(self, language_repo: LanguageRepo):
        self._language_repo = language_repo

    def handle(self, request):
        with self._language_repo.session() as s:
            language_name = request.headers.get('X-Locale', 'ru')
            languages = self._language_repo.filter_by_name(language_name)
            request.language = None if not languages else languages[0]
