from src.validation_rules.feature_type.create import (
    CreateFeatureTypeData,
    CreateFeatureTypeDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.serializers.feature_type import FeatureTypeSerializer
from src.constants.status_codes import OK_CODE
from src.services.feature_type import FeatureTypeService
from src.views.base import PaginatableView, ValidatableView


class FeatureTypeListView(ValidatableView[CreateFeatureTypeData], PaginatableView):
    def __init__(
        self,
        validator: CreateFeatureTypeDataValidator,
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

        raw_intl = request.args.get("raw_intl") == "1"
        serialized_feature_types = [
            self._serializer_cls(feature_type)
            .in_language(None if raw_intl else request.language)
            .serialize()
            for feature_type in feature_types
        ]
        return {"data": serialized_feature_types, "meta": meta}, OK_CODE

    def post(self, request: Request):
        valid_data = self._validate(request.get_json())
        feature_type = self._service.create(valid_data, user=request.user)
        serialized_feature_type = self._serializer_cls(feature_type).serialize()
        return {"data": serialized_feature_type}, OK_CODE
