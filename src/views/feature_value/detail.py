from src.validation_rules.feature_value.update import (
    UpdateFeatureValueDataValidator,
    UpdateFeatureValueData,
)
from src.utils.request import Request
from src.services.feature_value import FeatureValueService
from src.serializers.feature_value import FeatureValueSerializer
from typing import Type

from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE


class FeatureValueDetailView(ValidatableView[UpdateFeatureValueData]):
    def __init__(
        self,
        validator: UpdateFeatureValueDataValidator,
        service: FeatureValueService,
        serializer_cls: Type[FeatureValueSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, feature_value_id: int):
        try:
            feature_value = self._service.get_one(feature_value_id)
            should_get_raw_intl_field = request.args.get("raw_intl") == "1"
            serialized_feature_value = (
                self._serializer_cls(feature_value)
                .in_language(None if should_get_raw_intl_field else request.language)
                .with_serialized_feature_type()
                .serialize()
            )
            return {"data": serialized_feature_value}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, feature_value_id: int):
        try:
            valid_data = self._validate(request.get_json())
            feature_value = self._service.update(
                feature_value_id, valid_data, user=request.user
            )
            serialized_feature_value = (
                self._serializer_cls(feature_value)
                .with_serialized_feature_type()
                .serialize()
            )
            return {"data": serialized_feature_value}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.FeatureTypeInvalid:
            raise InvalidEntityFormat({"feature_type": "errors.invalidID"})

    def delete(self, request: Request, feature_value_id: int):
        try:
            self._service.delete(feature_value_id, user=request.user)
            return {}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, feature_value_id: int):
        try:
            self._service.get_one(feature_value_id)
            return {}, OK_CODE
        except self._service.FeatureValueNotFound:
            return {}, NOT_FOUND_CODE
