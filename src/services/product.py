from src.validation_rules.product.create import CreateProductData
from src.validation_rules.product.update import UpdateProductData
from typing import List
from src.services.decorators import allow_roles
from src.repos.product import ProductRepo
from src.repos.product_type import ProductTypeRepo
from src.repos.feature_value import FeatureValueRepo
from src.policies.feature_values import FeatureValuesPolicy


class ProductService:
    def __init__(
        self,
        repo: ProductRepo,
        product_type_repo: ProductTypeRepo,
        feature_value_repo: FeatureValueRepo,
        feature_values_policy: FeatureValuesPolicy,
    ):
        self._repo = repo
        self._product_type_repo = product_type_repo
        self._feature_value_repo = feature_value_repo
        self._feature_values_policy = feature_values_policy

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateProductData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                product_type = self._product_type_repo.get_by_id(
                    data["product_type_id"], session=s
                )
                feature_values = self._feature_value_repo.filter_by_ids(
                    data["feature_values"], session=s
                )

                if not self._feature_values_policy.are_allowed_if_product_type_is(
                    feature_values, product_type
                ):
                    raise self.FeatureValuesInvalid()

                return self._repo.add_product(
                    data["price"],
                    data["discount"],
                    data["quantity"],
                    data["images"],
                    product_type,
                    feature_values,
                    session=s,
                )
        except self._feature_value_repo.DoesNotExist:
            raise self.FeatureValuesInvalid()
        except self._product_type_repo.DoesNotExist:
            raise self.ProductTypeInvalid()

    @allow_roles(["admin", "manager"])
    def update(self, id_: int, data: UpdateProductData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                product_type = self._product_type_repo.get_by_id(
                    data["product_type_id"], session=s
                )
                feature_values = self._feature_value_repo.filter_by_ids(
                    data["feature_values"], session=s
                )

                if not self._feature_values_policy.are_allowed_if_product_type_is(
                    feature_values, product_type
                ):
                    raise self.FeatureValuesInvalid()

                return self._repo.update_product(
                    id_,
                    data["price"],
                    data["discount"],
                    data["quantity"],
                    data["images"],
                    product_type,
                    feature_values,
                    session=s,
                )
        except self._feature_value_repo.DoesNotExist:
            raise self.FeatureValuesInvalid()
        except self._product_type_repo.DoesNotExist:
            raise self.ProductTypeInvalid()

    def get_all(
        self,
        product_type_id: int = None,
        available=False,
        deleted=False,
        offset: int = None,
        limit: int = None,
    ):
        return self._repo.get_all(
            available=available,
            product_type_id=product_type_id,
            deleted=deleted,
            offset=offset,
            limit=limit,
        )

    def get_by_ids(self, ids: List[int]):
        return self._repo.filter_by_ids(ids)

    def get_one(self, id_: int, deleted=False):
        try:
            return self._repo.get_by_id(id_, deleted=deleted)
        except self._repo.DoesNotExist:
            raise self.ProductNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete(id_, forever=forever)
        except self._repo.DoesNotExist:
            raise self.ProductNotFound()

    @allow_roles(["admin", "manager"])
    def delete_forever(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete_forever(id_)
        except self._repo.DoesNotExist:
            raise self.ProductNotFound()

    class ProductNotFound(Exception):
        pass

    class FeatureValuesInvalid(Exception):
        pass

    class ProductTypeInvalid(Exception):
        pass

