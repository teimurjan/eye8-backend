from src.errors import InvalidEntityFormat
from src.constants.status_codes import OK_CODE
from src.views.base import PaginatableView
from src.services.product import ProductService
from src.serializers.product import ProductSerializer
from src.utils.number import parse_int


class ProductByProductTypeView(PaginatableView):
    def __init__(self, service: ProductService, serializer_cls: ProductSerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, product_type_id):
        products = self._service.get_for_product_type(product_type_id)

        serialized_product_types = [
            self
            ._serializer_cls(product)
            .in_language(request.language)
            .with_serialized_feature_values()
            .with_serialized_product_type()
            .serialize()
            for product in products
        ]

        return {'data': serialized_product_types}, OK_CODE
