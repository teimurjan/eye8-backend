from src.models import User
from src.models.order.order_item import OrderItem
from src.models.product import Product
from src.serializers.feature_value import FeatureValueSerializer
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
        self._promo_code = order.promo_code
        self._init_relation_safely('_items', order, 'items')
        self._created_on = order.created_on
        self._updated_on = order.updated_on
        self._is_deleted = order.is_deleted

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'items': self._serialize_items(),
            'user': self._serialize_user(),
            'user_name': self._user_name,
            'user_phone_number': self._user_phone_number,
            'user_address': self._user_address,
            'status': self._status,
            'promo_code': {
                'value': self._promo_code.value,
                'id': self._promo_code.id,
                'discount': self._promo_code.discount,
                'amount': self._promo_code.amount,
                'products': self._serialize_products(),
            } if self._promo_code else None,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
            'is_deleted': self._is_deleted,
        })

    def with_serialized_user(self):
        from src.serializers.user import UserSerializer
        self._with_serialized_relation('_user', User, UserSerializer)
        return self

    def _serialize_user(self):
        return self._serialize_relation('_user', User)

    def _serialize_products(self):
        if (self._promo_code and self._get_relation_safely(self._promo_code, 'products')):
            return [product.id for product in self._promo_code.products]
        return None

    def with_serialized_items(self):
        items = self._get_relation_safely(self, '_items')
        if items is None:
            return self

        serialized_items = []
        is_completed = self._status == 'completed'
        for item in items:
            serialized_items.append({
                'id': item.id,
                'product_price_per_item': item.product.price if not is_completed and item.product else item.product_price_per_item,
                'product_discount': item.product.discount if not is_completed and item.product else item.product_discount,
                'product_upc': item.product.upc if not is_completed and item.product else item.product_upc,
                'product': ProductSerializer(item.product).in_language(self._language).with_serialized_product_type().only(['id', 'quantity', 'product_type']).serialize() if item.product else None,
                'quantity': item.quantity,
            })
        self._items = serialized_items

        return self

    def _serialize_items(self):
        items = getattr(self, '_items')
        if items is None:
            return None

        return list(map(lambda item: item.id if isinstance(item, OrderItem) else item, self._items))
