from src.utils.request import Request


class LanguageHttpMiddleware:
    def handle(self, request: Request):
        request.language = request.headers.get("X-Locale", "ru")
