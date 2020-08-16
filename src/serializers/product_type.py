from src.models.category import Category
from src.models.feature_type import FeatureType
from src.models.product import Product
from src.serializers.category import CategorySerializer
from src.serializers.feature_type import FeatureTypeSerializer
from src.serializers.intl import IntlSerializer
from src.serializers.product import ProductSerializer


class ProductTypeSerializer(IntlSerializer):
    def __init__(self, product_type):
        super().__init__()
        self._id = product_type.id
        self._names = product_type.names
        self._descriptions = product_type.descriptions
        self._short_descriptions = product_type.short_descriptions
        self._instagram_links = product_type.instagram_links
        self._image = product_type.image
        self._categories = product_type.categories
        self._feature_types = product_type.feature_types
        # When called from ProductTypeSerializer product.product_type causes DetachedInstanceError
        self._init_relation_safely(
            '_products',
            product_type,
            'products',
            None
        )
        self._slug = product_type.slug
        self._is_deleted = product_type.is_deleted
        self._created_on = product_type.created_on
        self._updated_on = product_type.updated_on
        self._is_deleted = product_type.is_deleted

    def serialize(self):
        return self._filter_fields({
            'id': self._id,
            'name': self._serialize_name(),
            'description': self._serialize_description(),
            'short_description': self._serialize_short_description(),
            'instagram_links': self._serialize_instagram_links(),
            'image': self._image,
            'categories': self._serialize_categories(),
            'feature_types': self._serialize_feature_types(),
            'products': self._serialize_products(),
            'slug': self._slug,
            'is_deleted': self._is_deleted,
            'created_on': self._created_on,
            'updated_on': self._updated_on,
            'is_deleted': self._is_deleted,
        })

    def _serialize_name(self):
        return self._get_intl_field_from(self._names)

    def _serialize_description(self):
        return self._get_intl_field_from(self._descriptions)

    def _serialize_short_description(self):
        return self._get_intl_field_from(self._short_descriptions)

    def _serialize_instagram_links(self):
        return [{'id': instagram_link.id, 'link': instagram_link.link} for instagram_link in self._instagram_links]

    def with_serialized_categories(self):
        self._with_serialized_relations(
            '_categories',
            Category,
            CategorySerializer,
            lambda serializer: serializer.in_language(self._language)
        )

        return self

    def _serialize_categories(self):
        return self._serialize_relations('_categories', Category)

    def with_serialized_feature_types(self):
        self._with_serialized_relations(
            '_feature_types',
            FeatureType,
            FeatureTypeSerializer,
            lambda serializer: serializer.in_language(self._language)
        )

        return self

    def _serialize_feature_types(self):
        return self._serialize_relations('_feature_types', FeatureType)

    def _serialize_products(self):
        return self._serialize_relations('_products', Product)

    def with_serialized_products(self):
        self._with_serialized_relations(
            '_products',
            Product,
            ProductSerializer,
            lambda serializer: serializer.in_language(self._language)
        )

        return self
