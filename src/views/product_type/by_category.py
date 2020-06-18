from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService
from src.utils.number import parse_int
from src.views.base import PaginatableView
from src.views.product_type.list import get_sorting_type_from_request


class ProductTypeByCategoryView(PaginatableView):
    def __init__(self, service: ProductTypeService, serializer_cls: ProductTypeSerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, category_slug):
        pagination_data = self._get_pagination_data(request)
        sorting_type = get_sorting_type_from_request(request)

        meta = None
        product_types = []

        if pagination_data:
            product_types, count = self._service.get_all_by_category(
                category_slug,
                sorting_type,
                offset=pagination_data['offset'],
                limit=pagination_data['limit']
            )
            meta = self._get_meta(
                count,
                pagination_data['page'],
                pagination_data['limit']
            )
        else:
            product_types, count = self._service.get_all_by_category(category_slug, sorting_type)

        serialized_product_types = [
            self
            ._serializer_cls(product_type)
            .add_products(product_type.products)
            .in_language(request.language)
            .serialize()
            for product_type in product_types
        ]

        return {'data': serialized_product_types, 'meta': meta}, OK_CODE
