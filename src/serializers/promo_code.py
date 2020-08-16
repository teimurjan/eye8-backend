from src.models.feature_type import FeatureType
from src.models.product import Product
from src.serializers.intl import IntlSerializer
from src.serializers.feature_type import FeatureTypeSerializer
from src.serializers.product import ProductSerializer


class PromoCodeSerializer(IntlSerializer):
    def __init__(self, promo_code):
        super().__init__()
        self._id = promo_code.id
        self._discount = promo_code.discount
        self._amount = promo_code.amount
        self._value = promo_code.value
        self._is_active = promo_code.is_active
        self._disable_on_use = promo_code.disable_on_use
        self._products = promo_code.products
        self._created_on = promo_code.created_on
        self._updated_on = promo_code.updated_on
        self._is_deleted = promo_code.is_deleted

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'discount': self._discount,
            'amount': self._amount,
            'value': self._value,
            'is_active': self._is_active,
            'disable_on_use': self._disable_on_use,
            'products': self._serialize_products(),
            'created_on': self._created_on,
            'updated_on': self._updated_on,
            'is_deleted': self._is_deleted,
        })

    def _serialize_products(self):
        return self._serialize_relations('_products', Product)

    def with_serialized_products(self):
        self._with_serialized_relations(
            '_products',
            Product,
            ProductSerializer,
            lambda serializer: serializer.in_language(self._language).with_serialized_product_type()
        )

        return self
