from src.validation_rules.category.create import (
    CreateCategoryData,
    CreateCategoryDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.serializers.category import CategorySerializer
from src.services.category import CategoryService
from src.views.base import ValidatableView
from src.constants.status_codes import OK_CODE


class CategoryListView(ValidatableView[CreateCategoryData]):
    def __init__(
        self,
        validator: CreateCategoryDataValidator,
        service: CategoryService,
        serializer_cls: Type[CategorySerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        categories = self._service.get_all()
        should_get_raw_intl_field = request.args.get("raw_intl") == "1"
        serialized_categories = [
            self._serializer_cls(category)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for category in categories
        ]
        return {"data": serialized_categories}, OK_CODE

    def post(self, request: Request):
        valid_data = self._validate(request.get_json())
        category = self._service.create(valid_data, user=request.user)
        serialized_category = self._serializer_cls(category).serialize()
        return {"data": serialized_category}, OK_CODE
