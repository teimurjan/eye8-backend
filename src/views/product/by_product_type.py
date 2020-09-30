from src.utils.request import Request
from typing import Type
from src.constants.status_codes import OK_CODE
from src.views.base import PaginatableView
from src.services.product import ProductService
from src.serializers.product import ProductSerializer


class ProductByProductTypeView(PaginatableView):
    def __init__(
        self, service: ProductService, serializer_cls: Type[ProductSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, product_type_id: int):
        available = request.args.get("available") == "1"

        products, _ = self._service.get_all(
            product_type_id=product_type_id, available=available
        )

        serialized_product_types = [
            self._serializer_cls(product)
            .in_language(request.language)
            .with_serialized_feature_values()
            .with_serialized_product_type()
            .serialize()
            for product in products
        ]

        return {"data": serialized_product_types}, OK_CODE
