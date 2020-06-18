from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import OK_CODE


class CategoryListView(ValidatableView):
    def __init__(self, validator, service, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        categories = self._service.get_all()
        should_get_raw_intl_field = request.args.get('raw_intl') == '1'
        serialized_categories = [
            self
            ._serializer_cls(category)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for category in categories
        ]
        return {'data': serialized_categories}, OK_CODE

    def post(self, request):
        data = request.get_json()
        self._validate(data)
        category = self._service.create(data, user=request.user)
        serialized_category = (
            self
            ._serializer_cls(category)
            .serialize()
        )
        return {'data': serialized_category}, OK_CODE

