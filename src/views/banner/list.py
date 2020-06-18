from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class BannerListView(ValidatableView):
    def __init__(self, validator, service, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        banners = self._service.get_all()
        should_get_raw_intl_field = request.args.get('raw_intl') == '1'
        serialized_banners = [
            self
            ._serializer_cls(category)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for category in banners
        ]
        return {'data': serialized_banners}, OK_CODE

    def post(self, request):
        data = {
            **parse_json_from_form_data(request.form),
            'image': request.files.get('image'),
        }
        self._validate(data)
        banner = self._service.create(data, user=request.user)
        serialized_banners = (
            self
            ._serializer_cls(banner)
            .serialize()
        )
        return {'data': serialized_banners}, OK_CODE
