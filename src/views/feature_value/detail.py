from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE, UNPROCESSABLE_ENTITY_CODE


class FeatureValueDetailView(ValidatableView):
    def __init__(self, validator, service, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, feature_value_id):
        try:
            feature_value = self._service.get_one(feature_value_id)
            should_get_raw_intl_field = request.args.get('raw_intl') == '1'
            serialized_feature_value = (
                self.
                _serializer_cls(feature_value)
                .in_language(None if should_get_raw_intl_field else request.language)
                .with_serialized_feature_type()
                .serialize()
            )
            return {'data': serialized_feature_value}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request, feature_value_id):
        try:
            data = request.get_json()
            self._validate(data)
            feature_value = self._service.update(feature_value_id, data, user=request.user)
            serialized_feature_value = (
                self
                ._serializer_cls(feature_value)
                .with_serialized_feature_type()
                .serialize()
            )
            return {'data': serialized_feature_value}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.FeatureTypeInvalid:
            raise InvalidEntityFormat({'feature_type': 'errors.invalidID'})

    def delete(self, request, feature_value_id):
        try:
            self._service.delete(feature_value_id, user=request.user)
            return {}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request, feature_value_id):
        try:
            self._service.get_one(feature_value_id)
            return {}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE