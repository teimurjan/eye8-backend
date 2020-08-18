from src.models.product_type import ProductType
from src.models.feature_value import FeatureValue
from typing import List
from src.repos.feature_type import FeatureTypeRepo


class FeatureValuesPolicy:
    def __init__(self, feature_type_repo: FeatureTypeRepo):
        self._feature_type_repo = feature_type_repo

    def are_allowed_if_product_type_is(
        self, feature_values: List[FeatureValue], product_type: ProductType
    ):
        product_type_feature_types_ids = [
            feature_type.id for feature_type in product_type.feature_types
        ]
        feature_types_ids = [
            feature_value.feature_type.id for feature_value in feature_values
        ]

        return set(product_type_feature_types_ids) == set(feature_types_ids)
