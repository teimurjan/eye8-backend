from src.constants.status_codes import OK_CODE


class AuthCheckView:
    def get(self, request):
        return {}, OK_CODE
