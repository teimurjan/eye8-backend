from src.utils.request import Request
from typing import Type

from cerberus.validator import Validator
from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.order import OrderSerializer
from src.services.order import OrderService
from src.views.base import PaginatableView, ValidatableView


class OrderListView(ValidatableView, PaginatableView):
    def __init__(
        self,
        validator: Validator,
        service: OrderService,
        serializer_cls: Type[OrderSerializer],
    ):
        super().__init__(validator)
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request: Request):
        pagination_data = self._get_pagination_data(request)

        meta = None
        orders = []

        if pagination_data:
            orders, count = self._service.get_all(
                offset=pagination_data["offset"],
                limit=pagination_data["limit"],
                user=request.user,
            )
            meta = self._get_meta(
                count, pagination_data["page"], pagination_data["limit"]
            )
        else:
            orders, _ = self._service.get_all(user=request.user)

        serialized_products = [
            self._serializer_cls(order).with_serialized_user().serialize()
            for order in orders
        ]
        return {"data": serialized_products, "meta": meta}, OK_CODE

    def post(self, request: Request):
        try:
            data = request.get_json()
            self._validate(data)
            order = self._service.create(data, request.user)
            serialized_product = (
                self._serializer_cls(order).with_serialized_user().serialize()
            )
            return {"data": serialized_product}, OK_CODE
        except self._service.ProductInvalid:
            raise InvalidEntityFormat({"product": "errors.invalidID"})
        except self._service.PromoCodeInvalid:
            raise InvalidEntityFormat({"promo_code": "errors.invalidID"})
