from src.utils.request import Request
from typing import Type
from src.serializers.category import CategorySerializer
from src.services.category import CategoryService
from cerberus.validator import Validator
from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE


class CategoryDetailView(ValidatableView):
    def __init__(
        self,
        validator: Validator,
        service: CategoryService,
        serializer_cls: Type[CategorySerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, category_id: int):
        try:
            category = self._service.get_one(category_id)
            should_get_raw_intl_field = request.args.get("raw_intl") == "1"
            serialized_category = (
                self._serializer_cls(category)
                .in_language(None if should_get_raw_intl_field else request.language)
                .serialize()
            )
            return {"data": serialized_category}, OK_CODE
        except self._service.CategoryNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, category_id: int):
        try:
            data = request.get_json()
            self._validate(data)
            category = self._service.update(category_id, data, user=request.user)
            serialized_category = self._serializer_cls(category).serialize()
            return {"data": serialized_category}, OK_CODE
        except self._service.CategoryNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CircularCategoryConnection:
            raise InvalidEntityFormat(
                {"parent_category_id": "errors.circularConnection"}
            )

    def delete(self, request: Request, category_id: int):
        try:
            self._service.delete(category_id, user=request.user)
            return {}, OK_CODE
        except self._service.CategoryNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CategoryWithChildrenIsUntouchable:
            raise InvalidEntityFormat({"children": "errors.hasChildren"})
        except self._service.CategoryWithProductTypesIsUntouchable:
            raise InvalidEntityFormat({"product_types": "errors.hasProductTypes"})

    def head(self, request: Request, category_id: int):
        try:
            self._service.get_one(category_id)
            return {}, OK_CODE
        except self._service.CategoryNotFound:
            return {}, NOT_FOUND_CODE
