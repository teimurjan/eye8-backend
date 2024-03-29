from src.utils.request import Request
from typing import Type
from src.constants.status_codes import OK_CODE
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService
from src.views.base import PaginatableView
from src.views.product_type.list import get_sorting_type_from_request


class ProductTypeByCategoryView(PaginatableView):
    def __init__(
        self, service: ProductTypeService, serializer_cls: Type[ProductTypeSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, category_slug: str):
        pagination_data = self._get_pagination_data(request)
        sorting_type = get_sorting_type_from_request(request)
        available = request.args.get("available") == "1"

        characteristic_values_ids = (
            [int(id) for id in request.args.getlist("characteristics")]
            if request.args.get("characteristics") is not None
            else None
        )

        meta = None
        product_types = []

        if pagination_data:
            product_types, count = self._service.get_all_by_category(
                category_slug,
                sorting_type,
                available=available,
                characteristic_values_ids=characteristic_values_ids,
                offset=pagination_data["offset"],
                limit=pagination_data["limit"],
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            product_types, count = self._service.get_all_by_category(
                category_slug,
                sorting_type,
                available=available,
                characteristic_values_ids=characteristic_values_ids,
            )

        serialized_product_types = [
            self._serializer_cls(product_type)
            .in_language(request.language)
            .with_serialized_categories()
            .with_serialized_feature_types()
            .with_serialized_characteristic_values()
            .chain(lambda s: s.with_serialized_products())
            .serialize()
            for product_type in product_types
        ]

        return {"data": serialized_product_types, "meta": meta}, OK_CODE
