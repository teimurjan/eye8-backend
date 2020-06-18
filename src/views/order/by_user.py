from src.constants.status_codes import OK_CODE
from src.errors import InvalidEntityFormat
from src.serializers.order import OrderSerializer
from src.services.order import OrderService
from src.utils.number import parse_int
from src.views.base import PaginatableView


class OrderByUserView(PaginatableView):
    def __init__(self, service: OrderService, serializer_cls: OrderSerializer):
        self._service = service
        self._serializer_cls = serializer_cls

    def get(self, request, user_id):
        pagination_data = self._get_pagination_data(request)

        meta = None
        orders = []

        if pagination_data:
            orders, count = self._service.get_for_user(
                user_id,
                offset=pagination_data['offset'],
                limit=pagination_data['limit'],
                user=request.user
            )
            meta = self._get_meta(
                count,
                pagination_data['page'],
                pagination_data['limit']
            )
        else:
            orders, count = self._service.get_for_user(
                user_id, user=request.user)

        serialized_orders = [
            self
            ._serializer_cls(order)
            .in_language(request.language)
            .with_serialized_items()
            .with_serialized_user()
            .serialize()
            for order in orders
        ]

        return {'data': serialized_orders, 'meta': meta}, OK_CODE
