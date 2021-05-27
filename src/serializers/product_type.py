from src.models.characteristic_value import CharacteristicValue
from src.models.category import Category
from src.models.feature_type import FeatureType
from src.models.product import Product
from src.serializers.category import CategorySerializer
from src.serializers.feature_type import FeatureTypeSerializer
from src.serializers.intl import IntlSerializer
from src.serializers.product import ProductSerializer
from src.serializers.characteristic import CharacteristicSerializer


class ProductTypeSerializer(IntlSerializer):
    def __init__(self, product_type):
        super().__init__()
        self._id = product_type.id
        self._name_en = product_type.name_en
        self._name_ru = product_type.name_ru
        self._description_en = product_type.description_en
        self._description_ru = product_type.description_ru
        self._short_description_en = product_type.short_description_en
        self._short_description_ru = product_type.short_description_ru
        self._instagram_links = product_type.instagram_links
        self._image = product_type.image
        self._categories = product_type.categories
        self._feature_types = product_type.feature_types
        self._characteristic_values = product_type.characteristic_values
        # When called from ProductSerializer product.product_type causes DetachedInstanceError
        self._init_relation_safely("_products", product_type, "products", None)
        self._slug = product_type.slug
        self._is_deleted = product_type.is_deleted
        self._created_on = product_type.created_on
        self._updated_on = product_type.updated_on
        self._is_deleted = product_type.is_deleted

    def serialize(self):
        return self._filter_fields(
            {
                "id": self._id,
                "name": self._get_intl_field_from("name", self),
                "description": self._get_intl_field_from("description", self),
                "short_description": self._get_intl_field_from(
                    "short_description", self
                ),
                "instagram_links": self._serialize_instagram_links(),
                "image": self._image,
                "categories": self._serialize_categories(),
                "feature_types": self._serialize_feature_types(),
                "characteristic_values": self._serialize_characteristic_values(),
                "products": self._serialize_products(),
                "slug": self._slug,
                "is_deleted": self._is_deleted,
                "created_on": self._created_on,
                "updated_on": self._updated_on,
                "is_deleted": self._is_deleted,
            }
        )

    def _serialize_instagram_links(self):
        return [
            {"id": instagram_link.id, "link": instagram_link.link}
            for instagram_link in self._instagram_links
        ]

    def with_serialized_categories(self):
        self._with_serialized_relations(
            "_categories",
            CategorySerializer,
            lambda serializer: serializer.in_language(self._language),
        )

        return self

    def _serialize_categories(self):
        return self._serialize_relations("_categories", Category)

    def with_serialized_feature_types(self):
        self._with_serialized_relations(
            "_feature_types",
            FeatureTypeSerializer,
            lambda serializer: serializer.in_language(self._language),
        )

        return self

    def _serialize_feature_types(self):
        return self._serialize_relations("_feature_types", FeatureType)

    def with_serialized_characteristic_values(self):
        self._with_serialized_relations(
            "_characteristic_values",
            CharacteristicSerializer,
            lambda serializer: serializer.in_language(self._language),
        )

        return self

    def _serialize_characteristic_values(self):
        return self._serialize_relations("_characteristic_values", CharacteristicValue)

    def with_serialized_products(self):
        self._with_serialized_relations(
            "_products",
            ProductSerializer,
            lambda serializer: serializer.in_language(self._language),
        )

        return self

    def _serialize_products(self):
        return self._serialize_relations("_products", Product)
