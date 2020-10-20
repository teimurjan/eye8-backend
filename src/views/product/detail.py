from src.validation_rules.product.update import (
    UpdateProductData,
    UpdateProductDataValidator,
)
from typing import Type
from src.serializers.product import ProductSerializer
from src.services.product import ProductService
from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import (
    NOT_FOUND_CODE,
    OK_CODE,
)
from src.utils.json import parse_json_from_form_data
from src.utils.request import Request


class ProductDetailView(ValidatableView[UpdateProductData]):
    def __init__(
        self,
        validator: UpdateProductDataValidator,
        service: ProductService,
        serializer_cls: Type[ProductSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, product_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            product = self._service.get_one(product_id, deleted=deleted)
            serialized_product = (
                self._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .serialize()
            )
            return {"data": serialized_product}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request: Request, product_id: int):
        try:
            deleted = request.args.get("deleted") == "1"
            self._service.get_one(product_id, deleted=deleted)
            return {}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request: Request, product_id: int):
        try:
            valid_data = self._validate(
                data={
                    **parse_json_from_form_data(request.form),
                    "images": request.files.getlist("images")
                    or request.form.getlist("images"),
                }
            )
            product = self._service.update(product_id, valid_data, user=request.user)
            serialized_product = (
                self._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .serialize()
            )
            return {"data": serialized_product}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.FeatureValuesInvalid:
            raise InvalidEntityFormat({"feature_values": "errors.invalidID"})
        except self._service.ProductTypeInvalid:
            raise InvalidEntityFormat({"product_type": "errors.invalidID"})

    def delete(self, request: Request, product_id: int):
        try:
            forever = request.args.get("forever") == "1"
            self._service.delete(product_id, forever=forever, user=request.user)
            return {}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE
