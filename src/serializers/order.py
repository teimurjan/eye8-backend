from src.models import User
from src.models.order.order_item import OrderItem
from src.serializers.intl import IntlSerializer
from src.serializers.product import ProductSerializer


class OrderSerializer(IntlSerializer):
    def __init__(self, order):
        super().__init__()
        self._id = order.id
        self._user = order.user
        self._user_name = order.user_name
        self._user_phone_number = order.user_phone_number
        self._user_address = order.user_address
        self._status = order.status
        self._promo_code_value = order.promo_code_value
        self._promo_code_discount = order.promo_code_discount
        self._promo_code_amount = order.promo_code_amount
        self._promo_code_products_ids = order.promo_code_products_ids
        self._items = order.items
        self._created_on = order.created_on
        self._updated_on = order.updated_on
        self._is_deleted = order.is_deleted

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "items": self._serialize_items(),
                "user": self._serialize_user(),
                "user_name": self._user_name,
                "user_phone_number": self._user_phone_number,
                "user_address": self._user_address,
                "status": self._status,
                "promo_code_value": self._promo_code_value,
                "promo_code_discount": self._promo_code_discount,
                "promo_code_amount": self._promo_code_amount,
                "promo_code_products_ids": self._promo_code_products_ids,
                "created_on": self._created_on,
                "updated_on": self._updated_on,
                "is_deleted": self._is_deleted,
            }
        )

    def with_serialized_user(self):
        from src.serializers.user import UserSerializer

        self._with_serialized_relation("_user", User, UserSerializer)
        return self

    def _serialize_user(self):
        return self._serialize_relation("_user", User)

    def with_serialized_items(self):
        items = self._get_relation_safely(self, "_items")
        if items is None:
            return self

        serialized_items = []
        is_completed = self._status == "completed"
        for item in items:
            serialized_items.append(
                {
                    "id": item.id,
                    "product_price_per_item": (
                        item.product.price
                        if not is_completed and item.product
                        else item.product_price_per_item
                    ),
                    "product_discount": (
                        item.product.discount
                        if not is_completed and item.product
                        else item.product_discount
                    ),
                    "product": (
                        ProductSerializer(item.product)
                        .in_language(self._language)
                        .with_serialized_product_type()
                        .only(["id", "quantity", "product_type"])
                        .serialize()
                        if item.product
                        else None
                    ),
                    "quantity": item.quantity,
                }
            )
        self._items = serialized_items

        return self

    def _serialize_items(self):
        return self._serialize_relations("_items", OrderItem)
