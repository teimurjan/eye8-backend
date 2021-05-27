from src.constants.status_codes import OK_CODE


class LanguageListView:
    def get(self, request):
        return (
            {
                "data": [{id: "en", "name": "en"}, {"id": "ru", "name": "en"}],
                "meta": None,
            },
            OK_CODE,
        )
