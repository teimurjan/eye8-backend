from src.models.feature_value import FeatureValue
from src.models.product_type import ProductType
from src.serializers.feature_value import FeatureValueSerializer
from src.serializers.intl import IntlSerializer


class ProductSerializer(IntlSerializer):
    def __init__(self, product):
        super().__init__()
        self._id = product.id
        self._discount = product.discount
        self._price = product.price
        self._quantity = product.quantity
        self._upc = product.upc
        # When called from ProductTypeSerializer product.product_type causes DetachedInstanceError
        self._init_relation_safely(
            '_product_type',
            product,
            'product_type',
            product.product_type_id
        )
        self._images = product.images
        self._feature_values = product.feature_values
        self._created_on = product.created_on
        self._updated_on = product.updated_on
        self._is_deleted = product.is_deleted

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'discount': self._discount,
            'price': self._price,
            'quantity': self._quantity,
            'upc': self._upc,
            'product_type': self._serialize_product_type(),
            'images': self._serialize_images(),
            'feature_values': self._serialize_feature_values(),
            'created_on': self._created_on,
            'updated_on': self._updated_on,
            'is_deleted': self._is_deleted,
        })

    def with_serialized_product_type(self):
        from src.serializers.product_type import ProductTypeSerializer
        self._with_serialized_relation(
            '_product_type',
            ProductType,
            ProductTypeSerializer,
            lambda serializer: (
                serializer
                .in_language(self._language)
                .only(['id', 'name', 'image', 'category', 'feature_types', 'slug'])
            )
        )
        return self

    def _serialize_product_type(self):
        return self._serialize_relation('_product_type', ProductType)

    def _serialize_images(self):
        return [image.image for image in self._images]

    def with_serialized_feature_values(self):
        self._with_serialized_relations(
            '_feature_values',
            FeatureValue,
            FeatureValueSerializer,
            lambda serializer: (
                serializer
                .in_language(self._language)
                .with_serialized_feature_type()
            )
        )
        return self

    def _serialize_feature_values(self):
        return self._serialize_relations('_feature_values', FeatureValue)
