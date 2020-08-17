from src.utils.request import Request
from typing import Type
from src.serializers.product import ProductSerializer
from cerberus.validator import Validator
from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.product import ProductService
from src.utils.json import parse_json_from_form_data
from src.views.base import PaginatableView, ValidatableView


class ProductListView(ValidatableView, PaginatableView):
    def __init__(
        self,
        validator: Validator,
        service: ProductService,
        serializer_cls: Type[ProductSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        pagination_data = self._get_pagination_data(request)
        ids = request.args.getlist("ids", type=int)

        meta = None
        products = []

        if ids:
            products = self._service.get_by_ids(ids)
        elif pagination_data:
            products, count = self._service.get_all(
                offset=pagination_data["offset"], limit=pagination_data["limit"]
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            products, _ = self._service.get_all()

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
            data = {
                **parse_json_from_form_data(request.form),
                "images": request.files.getlist("images"),
            }
            self._validate(data)
            product = self._service.create(data, user=request.user)
            serialized_product = (
                self._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .serialize()
            )
            return {"data": serialized_product}, OK_CODE
        except self._service.FeatureValuesInvalid:
            raise InvalidEntityFormat({"feature_values": "errors.invalidID"})
        except self._service.ProductTypeInvalid:
            raise InvalidEntityFormat({"product_type": "errors.invalidID"})
        except self._service.SameUPC:
            raise InvalidEntityFormat({"upc": "errors.sameUPC"})
