from src.views.base import ValidatableView
from src.errors import InvalidEntityFormat
from src.constants.status_codes import NOT_FOUND_CODE, OK_CODE, UNPROCESSABLE_ENTITY_CODE
from src.utils.json import parse_json_from_form_data


class ProductDetailView(ValidatableView):
    def __init__(self, validator, service, serializer_cls):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, product_id):
        try:
            product = self._service.get_one(product_id)
            serialized_product = (
                self
                ._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .serialize()
            )
            return {'data': serialized_product}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request, product_id):
        try:
            self._service.get_one(product_id)
            return {}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request, product_id):
        try:
            data = {
                **parse_json_from_form_data(request.form),
                'images': request.files.getlist('images')
            }
            self._validate(data)
            product = self._service.update(product_id, data, user=request.user)
            serialized_product = (
                self
                ._serializer_cls(product)
                .in_language(request.language)
                .with_serialized_product_type()
                .serialize()
            )
            return {'data': serialized_product}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.FeatureValuesInvalid:
            raise InvalidEntityFormat({'feature_values': 'errors.invalidID'})
        except self._service.ProductTypeInvalid:
            raise InvalidEntityFormat({'product_type': 'errors.invalidID'})
        except self._service.SameUPC:
            raise InvalidEntityFormat({'upc': 'errors.sameUPC'})

    def delete(self, request, product_id):
        try:
            self._service.delete(product_id, user=request.user)
            return {}, OK_CODE
        except self._service.ProductNotFound:
            return {}, NOT_FOUND_CODE
