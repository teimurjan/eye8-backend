from src.utils.request import Request
from typing import Type
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService


class ProductTypeSlugView:
    def __init__(
        self, service: ProductTypeService, serializer_cls: Type[ProductTypeSerializer]
    ):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request, slug: str):
        try:
            product_type = self._service.get_one_by_slug(slug)
            serialized_product_type = (
                self._serializer_cls(product_type)
                .in_language(request.language)
                .with_serialized_categories()
                .serialize()
            )
            return {"data": serialized_product_type}, OK_CODE
        except self._service.ProductTypeNotFound:
            return {}, NOT_FOUND_CODE
