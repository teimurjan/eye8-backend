from src.utils.request import Request
from src.repos.language import LanguageRepo


class LanguageHttpMiddleware:
    def __init__(self, language_repo: LanguageRepo):
        self._language_repo = language_repo

    def handle(self, request: Request):
        name = request.headers.get("X-Locale", "ru")
        languages = self._language_repo.filter_by_name(name)
        request.language = languages[0]
