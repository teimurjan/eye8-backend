from typing import Callable


class ReInitMiddleware:
    def __init__(self, is_initialized: Callable[[], bool], re_init: Callable[[], None]):
        self._is_initialized = is_initialized
        self._re_init = re_init

    def handle(self, request):
        if not self._is_initialized():
            self._re_init()
