from src.utils.request import Request
from typing import Type
from src.serializers.feature_type import FeatureTypeSerializer
from cerberus.validator import Validator
from src.constants.status_codes import OK_CODE
from src.services.feature_type import FeatureTypeService
from src.views.base import PaginatableView, ValidatableView


class FeatureTypeListView(ValidatableView, PaginatableView):
    def __init__(
        self,
        validator: Validator,
        service: FeatureTypeService,
        serializer_cls: Type[FeatureTypeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        pagination_data = self._get_pagination_data(request)

        meta = None
        feature_types = []

        if pagination_data:
            feature_types, count = self._service.get_all(
                offset=pagination_data["offset"], limit=pagination_data["limit"]
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            feature_types, _ = self._service.get_all()

        should_get_raw_intl_field = request.args.get("raw_intl") == "1"
        serialized_feature_types = [
            self._serializer_cls(feature_type)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for feature_type in feature_types
        ]
        return {"data": serialized_feature_types, "meta": meta}, OK_CODE

    def post(self, request: Request):
        data = request.get_json()
        self._validate(data)
        feature_type = self._service.create(data, user=request.user)
        serialized_feature_type = self._serializer_cls(feature_type).serialize()
        return {"data": serialized_feature_type}, OK_CODE
