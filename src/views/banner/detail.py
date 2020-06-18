from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.errors import InvalidEntityFormat
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class BannerDetailView(ValidatableView):
    def __init__(self, validator, service, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, banner_id):
        try:
            banner = self._service.get_one(banner_id)
            should_get_raw_intl_field = request.args.get('raw_intl') == '1'
            serialized_banner = (
                self
                ._serializer_cls(banner)
                .in_language(None if should_get_raw_intl_field else request.language)
                .serialize()
            )
            return {'data': serialized_banner}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request, banner_id):
        try:
            data = {
                **parse_json_from_form_data(request.form),
                'image': request.files.get('image') or request.form.get('image'),
            }

            self._validate(data)
            banner = self._service.update(banner_id, data, user=request.user)
            serialized_banner = (
                self
                ._serializer_cls(banner)
                .serialize()
            )
            return {'data': serialized_banner}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def delete(self, request, banner_id):
        try:
            self._service.delete(banner_id, user=request.user)
            return {}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request, banner_id):
        try:
            self._service.get_one(banner_id)
            return {}, OK_CODE
        except self._service.BannerNotFound:
            return {}, NOT_FOUND_CODE
