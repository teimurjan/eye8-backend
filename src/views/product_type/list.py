from werkzeug import Request

from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.services.product_type import ProductTypeService
from src.utils.json import parse_json_from_form_data
from src.utils.sorting import ProductTypeSortingType
from src.views.base import PaginatableView, ValidatableView


def get_sorting_type_from_request(request: Request) -> ProductTypeSortingType:
    sort_by = request.args.get('sort_by')
    if sort_by == 'price_asc':
        return ProductTypeSortingType.PRICE_ASCENDING
    if sort_by == 'price_desc':
        return ProductTypeSortingType.PRICE_DESCENDING
    if sort_by == 'recent':
        return ProductTypeSortingType.NEWLY_ADDED

    return ProductTypeSortingType.DEFAULT


class ProductTypeListView(ValidatableView, PaginatableView):
    def __init__(
        self,
        validator,
        service: ProductTypeService,
        serializer_cls
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request):
        product_types = []
        meta = None
        sorting_type = get_sorting_type_from_request(request)
        only_fields = request.args.getlist('fields')
        only_available = request.args.get('available') == '1'
        serialize_products = request.args.get('products') == '1'
        should_get_raw_intl_field = request.args.get('raw_intl') == '1'

        pagination_data = self._get_pagination_data(request)
        if pagination_data:
            product_types, count = self._service.get_all(
                only_available=only_available,
                sorting_type=sorting_type,
                offset=pagination_data['offset'],
                limit=pagination_data['limit'],
            )
            meta = self._get_meta(
                count,
                pagination_data['page'],
                pagination_data['limit'],
            )
        else:
            product_types, _ = self._service.get_all(
                sorting_type=sorting_type,
            )

        serialized_product_types = [
            self
            ._serializer_cls(product_type)
            .in_language(None if should_get_raw_intl_field else request.language)
            .only(request.args.getlist('fields'))
            .chain(lambda s: s.with_serialized_products() if serialize_products else None)
            .serialize()
            for product_type in product_types
        ]
        return {'data': serialized_product_types, 'meta': meta}, OK_CODE

    def post(self, request):
        try:
            data = {
                **parse_json_from_form_data(request.form),
                'image': request.files.get('image'),
            }
            self._validate(data)
            product_type = self._service.create(data, user=request.user)
            serialized_product_type = (
                self
                ._serializer_cls(product_type)
                .with_serialized_feature_types()
                .serialize()
            )
            return {'data': serialized_product_type}, OK_CODE
        except self._service.CategoryInvalid:
            raise InvalidEntityFormat({'category_id': 'errors.invalidID'})
        except self._service.FeatureTypesInvalid:
            raise InvalidEntityFormat({'feature_types': 'errors.invalidID'})
