from src.serializers.intl import IntlSerializer


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
        return self._filter_fields(
            {
                "id": self._id,
                "discount": self._discount,
                "amount": self._amount,
                "value": self._value,
                "is_active": self._is_active,
                "disable_on_use": self._disable_on_use,
                "products": [product.id for product in self._products],
                "created_on": self._created_on,
                "updated_on": self._updated_on,
                "is_deleted": self._is_deleted,
            }
        )
