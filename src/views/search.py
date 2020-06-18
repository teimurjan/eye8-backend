from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat


class SearchView:
    def __init__(self, category_service, product_type_service, category_serializer_cls, product_type_serializer_cls):
        self._category_service = category_service
        self._product_type_service = product_type_service
        self._category_serializer_cls = category_serializer_cls
        self._product_type_serializer_cls = product_type_serializer_cls

    def get(self, request, query: str):
        categories = self._category_service.search(query, request.language)
        product_types = self._product_type_service.search(
            query, request.language)
        should_get_raw_intl_field = request.args.get('raw_intl') == '1'
        serialized_categories = [
            self
            ._category_serializer_cls(product_type)
            .in_language(None if should_get_raw_intl_field else request.language)
            .serialize()
            for product_type in categories
        ]
        serialized_product_types = [
            self
            ._product_type_serializer_cls(product_type)
            .in_language(None if should_get_raw_intl_field else request.language)
            .only(['id', 'name', 'short_description', 'category', 'image', 'slug'])
            .serialize()
            for product_type in product_types
        ]
        return {'data': {'product_types': serialized_product_types, 'categories': serialized_categories}}, OK_CODE
