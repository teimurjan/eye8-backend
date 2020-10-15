from src.validation_rules.feature_value.create import (
    CreateFeatureValueData,
    CreateFeatureValueDataValidator,
)
from typing import Type
from src.serializers.feature_value import FeatureValueSerializer
from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.feature_value import FeatureValueService
from src.views.base import PaginatableView, ValidatableView


class FeatureValueListView(ValidatableView[CreateFeatureValueData], PaginatableView):
    def __init__(
        self,
        validator: CreateFeatureValueDataValidator,
        service: FeatureValueService,
        serializer_cls: Type[FeatureValueSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        pagination_data = self._get_pagination_data(request)

        meta = None
        feature_values = []

        if pagination_data:
            feature_values, count = self._service.get_all(
                offset=pagination_data["offset"], limit=pagination_data["limit"]
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            feature_values, _ = self._service.get_all()

        raw_intl = request.args.get("raw_intl") == "1"

        serialized_feature_values = [
            self._serializer_cls(feature_value)
            .in_language(None if raw_intl else request.language)
            .with_serialized_feature_type()
            .serialize()
            for feature_value in feature_values
        ]
        return {"data": serialized_feature_values, "meta": meta}, OK_CODE

    def post(self, request):
        try:
            valid_data = self._validate(request.get_json())
            feature_value = self._service.create(valid_data, user=request.user)
            serialized_feature_value = (
                self._serializer_cls(feature_value)
                .with_serialized_feature_type()
                .serialize()
            )
            return {"data": serialized_feature_value}, OK_CODE
        except self._service.FeatureTypeInvalid:
            raise InvalidEntityFormat({"feature_type_id": "errors.invalidID"})
