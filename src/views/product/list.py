from src.validation_rules.product.create import (
    CreateProductData,
    CreateProductDataValidator,
)
from src.utils.request import Request
from typing import Type
from src.serializers.product import ProductSerializer
from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.product import ProductService
from src.utils.json import parse_json_from_form_data
from src.views.base import PaginatableView, ValidatableView


class ProductListView(ValidatableView[CreateProductData], PaginatableView):
    def __init__(
        self,
        validator: CreateProductDataValidator,
        service: ProductService,
        serializer_cls: Type[ProductSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        pagination_data = self._get_pagination_data(request)
        available = request.args.get("available") == "1"

        meta = None
        products = []

        deleted = request.args.get("deleted") == "1"

        if request.args.get("ids") is not None:
            ids = request.args.getlist("ids", type=int)
            products = self._service.get_by_ids(ids)
        elif pagination_data:
            products, count = self._service.get_all(
                available=available,
                offset=pagination_data["offset"],
                limit=pagination_data["limit"],
                deleted=deleted,
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            products, _ = self._service.get_all(available=available, deleted=deleted)

        serialized_products = [
            self._serializer_cls(product)
            .in_language(request.language)
            .with_serialized_product_type()
            .with_serialized_feature_values()
            .serialize()
            for product in products
        ]
        return {"data": serialized_products, "meta": meta}, OK_CODE

    def post(self, request: Request):
        try:
            valid_data = self._validate(
                {
                    **parse_json_from_form_data(request.form),
                    "images": request.files.getlist("images"),
                }
            )
            product = self._service.create(valid_data, user=request.user)
            serialized_product = (
                self._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .with_serialized_feature_values()
                .serialize()
            )
            return {"data": serialized_product}, OK_CODE
        except self._service.FeatureValuesInvalid:
            raise InvalidEntityFormat({"feature_values": "errors.invalidID"})
        except self._service.ProductTypeInvalid:
            raise InvalidEntityFormat({"product_type": "errors.invalidID"})
