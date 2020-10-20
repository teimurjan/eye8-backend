from typing import Type

from src.constants.status_codes import OK_CODE
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService
from src.utils.request import Request
from src.views.base import PaginatableView


class ProductTypeSearchView(PaginatableView):
    def __init__(
        self, service: ProductTypeService, serializer_cls: Type[ProductTypeSerializer],
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, query: str):
        product_types = []
        meta = None
        only_fields = request.args.getlist("fields")
        available = request.args.get("available") == "1"
        raw_intl = request.args.get("raw_intl") == "1"
        deleted = request.args.get("deleted") == "1"

        pagination_data = self._get_pagination_data(request)
        if pagination_data:
            product_types, count = self._service.search(
                query=query,
                available=available,
                deleted=deleted,
                offset=pagination_data["offset"],
                limit=pagination_data["limit"],
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"],
            )
        else:
            product_types, _ = self._service.search(
                query=query, available=available, deleted=deleted,
            )

        serialized_product_types = [
            self._serializer_cls(product_type)
            .in_language(None if raw_intl else request.language)
            .only(only_fields)
            .serialize()
            for product_type in product_types
        ]
        return {"data": serialized_product_types, "meta": meta}, OK_CODE
