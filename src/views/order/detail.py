from src.constants.status_codes import (NOT_FOUND_CODE, OK_CODE,
                                        UNPROCESSABLE_ENTITY_CODE)
from src.errors import InvalidEntityFormat
from src.serializers.order import OrderSerializer
from src.services.order import OrderService
from src.utils.json import parse_json_from_form_data
from src.views.base import ValidatableView


class OrderDetailView(ValidatableView):
    def __init__(self, validator, service: OrderService, serializer_cls: OrderSerializer):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, order_id):
        try:
            order = self._service.get_one(order_id, user=request.user)

            serialized_order = (
                self
                ._serializer_cls(order)
                .in_language(request.language)
                .with_serialized_items()
                .with_serialized_user()
                .serialize()
            )
            return {'data': serialized_order}, OK_CODE
        except self._service.OrderNotFound:
            return {}, NOT_FOUND_CODE

    def put(self, request, order_id):
        try:
            data = request.get_json()
            self._validate(data)
            order = self._service.update(order_id, data, user=request.user)
            serialized_product = (
                self
                ._serializer_cls(order)
                .with_serialized_user()
                .serialize()
            )
            return {'data': serialized_product}, OK_CODE
        except self._service.OrderNotFound:
            return {}, NOT_FOUND_CODE
        except self._service.ProductInvalid:
            raise InvalidEntityFormat({'product': 'errors.invalidID'})
        except self._service.PromoCodeInvalid:
            raise InvalidEntityFormat({'promo_code': 'errors.invalidID'})

    def delete(self, request, order_id):
        try:
            self._service.delete(order_id, user=request.user)
            return {}, OK_CODE
        except self._service.OrderNotFound:
            return {}, NOT_FOUND_CODE

    def head(self, request, order_id):
        try:
            self._service.get_one(order_id, user=request.user)
            return {}, OK_CODE
        except self._service.OrderNotFound:
            return {}, NOT_FOUND_CODE
