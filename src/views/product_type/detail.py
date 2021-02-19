from src.validation_rules.product_type.update import (
    UpdateProductTypeData,
    UpdateProductTypeDataValidator,
)
from src.utils.request import Request
from typing import Type

from src.constants.status_codes import (
    NOT_FOUND_CODE,
    OK_CODE,
)
from src.errors import InvalidEntityFormat
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class ProductTypeDetailView(ValidatableView[UpdateProductTypeData]):
    def __init__(
        self,
        validator: UpdateProductTypeDataValidator,
        service: ProductTypeService,
        serializer_cls: Type[ProductTypeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, product_type_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            raw_intl = request.args.get("raw_intl") == "1"
            product_type = self._service.get_one(product_type_id, deleted=deleted)

            serialized_product_type = (
                self._serializer_cls(product_type)
                .in_language(None if raw_intl else request.language)
                .with_serialized_categories()
                .with_serialized_feature_types()
                .with_serialized_characteristic_values()
                .chain(lambda s: s.with_serialized_products())
                .serialize()
            )
            return {"data": serialized_product_type}, OK_CODE
        except self._service.ProductTypeNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, product_type_id: int):
        try:
            valid_data = self._validate(
                {
                    **parse_json_from_form_data(request.form),
                    "image": request.files.get("image") or request.form.get("image"),
                }
            )
            product_type = self._service.update(
                product_type_id, valid_data, user=request.user
            )
            serialized_product_type = (
                self._serializer_cls(product_type)
                .with_serialized_categories()
                .with_serialized_feature_types()
                .with_serialized_characteristic_values()
                .chain(lambda s: s.with_serialized_products())
                .serialize()
            )
            return {"data": serialized_product_type}, OK_CODE
        except self._service.ProductTypeNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.CategoryInvalid:
            raise InvalidEntityFormat({"category_id": "errors.invalidID"})
        except self._service.FeatureTypesInvalid:
            raise InvalidEntityFormat({"feature_types": "errors.invalidID"})

    def delete(self, request: Request, product_type_id: int):
        try:
            forever = request.args.get("forever") == "1"

            if forever:
                self._service.delete_forever(product_type_id, user=request.user)
            else:
                self._service.delete(product_type_id, user=request.user)

            return {}, OK_CODE
        except self._service.ProductTypeNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.ProductTypeWithProductsIsUntouchable:
            raise InvalidEntityFormat({"products": "errors.hasProducts"})

    def head(self, request: Request, product_type_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            self._service.get_one(product_type_id, deleted=deleted)

            return {}, OK_CODE
        except self._service.ProductTypeNotFound:
            return {}, NOT_FOUND_CODE
