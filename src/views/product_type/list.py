from src.validation_rules.product_type.create import (
    CreateProductTypeData,
    CreateProductTypeDataValidator,
)
from typing import Type

from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.product_type import ProductTypeSerializer
from src.services.product_type import ProductTypeService
from src.utils.json import parse_json_from_form_data
from src.utils.request import Request
from src.utils.sorting import ProductTypeSortingType
from src.views.base import PaginatableView, ValidatableView


def get_sorting_type_from_request(request: Request) -> ProductTypeSortingType:
    sort_by = request.args.get("sort_by")
    if sort_by == "price_asc":
        return ProductTypeSortingType.PRICE_ASCENDING
    if sort_by == "price_desc":
        return ProductTypeSortingType.PRICE_DESCENDING
    if sort_by == "recent":
        return ProductTypeSortingType.NEWLY_ADDED

    return ProductTypeSortingType.DEFAULT


class ProductTypeListView(ValidatableView[CreateProductTypeData], PaginatableView):
    def __init__(
        self,
        validator: CreateProductTypeDataValidator,
        service: ProductTypeService,
        serializer_cls: Type[ProductTypeSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        product_types = []
        meta = None
        sorting_type = get_sorting_type_from_request(request)
        only_fields = request.args.getlist("fields")
        available = request.args.get("available") == "1"
        raw_intl = request.args.get("raw_intl") == "1"
        deleted = request.args.get("deleted") == "1"

        pagination_data = self._get_pagination_data(request)
        if pagination_data:
            product_types, count = self._service.get_all(
                available=available,
                sorting_type=sorting_type,
                deleted=deleted,
                offset=pagination_data["offset"],
                limit=pagination_data["limit"],
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"],
            )
        else:
            product_types, _ = self._service.get_all(
                available=available, sorting_type=sorting_type, deleted=deleted,
            )

        serialized_product_types = [
            self._serializer_cls(product_type)
            .in_language(None if raw_intl else request.language)
            .only(only_fields)
            .with_serialized_categories()
            .with_serialized_feature_types()
            .with_serialized_characteristic_values()
            .chain(lambda s: s.with_serialized_products())
            .serialize()
            for product_type in product_types
        ]
        return {"data": serialized_product_types, "meta": meta}, OK_CODE

    def post(self, request: Request):
        try:
            valid_data = self._validate(
                {
                    **parse_json_from_form_data(request.form),
                    "image": request.files.get("image"),
                }
            )
            product_type = self._service.create(valid_data, user=request.user)
            serialized_product_type = (
                self._serializer_cls(product_type)
                .with_serialized_categories()
                .with_serialized_feature_types()
                .chain(lambda s: s.with_serialized_products())
                .serialize()
            )
            return {"data": serialized_product_type}, OK_CODE
        except self._service.CategoryInvalid:
            raise InvalidEntityFormat({"category_id": "errors.invalidID"})
        except self._service.FeatureTypesInvalid:
            raise InvalidEntityFormat({"feature_types": "errors.invalidID"})
