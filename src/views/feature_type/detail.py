from src.utils.request import Request
from src.services.feature_type import FeatureTypeService
from typing import Type
from src.serializers.feature_type import FeatureTypeSerializer
from cerberus.validator import Validator
from src.views.base import ValidatableView
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE


class FeatureTypeDetailView(ValidatableView):
    def __init__(
        self,
        validator: Validator,
        service: FeatureTypeService,
        serializer_cls: Type[FeatureTypeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, feature_type_id: int):
        try:
            feature_type = self._service.get_one(feature_type_id)
            should_get_raw_intl_field = request.args.get("raw_intl") == "1"
            serialized_feature_type = (
                self._serializer_cls(feature_type)
                .in_language(None if should_get_raw_intl_field else request.language)
                .serialize()
            )
            return {"data": serialized_feature_type}, OK_CODE
        except self._service.FeatureTypeNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, feature_type_id: int):
        try:
            data = request.get_json()
            self._validate(data)
            feature_type = self._service.update(
                feature_type_id, data, user=request.user
            )
            serialized_feature_type = self._serializer_cls(feature_type).serialize()
            return {"data": serialized_feature_type}, OK_CODE
        except self._service.FeatureTypeNotFound:
            return {}, NOT_FOUND_CODE

    def delete(self, request: Request, feature_type_id: int):
        try:
            self._service.delete(feature_type_id, user=request.user)
            return {}, OK_CODE
        except self._service.FeatureTypeNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, feature_type_id: int):
        try:
            self._service.get_one(feature_type_id)
            return {}, OK_CODE
        except self._service.FeatureTypeNotFound:
            return {}, NOT_FOUND_CODE
