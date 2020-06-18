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
        feature_values_policy: FeatureValuesPolicy
    ):
        self._repo = repo
        self._product_type_repo = product_type_repo
        self._feature_value_repo = feature_value_repo
        self._feature_values_policy = feature_values_policy

    @allow_roles(['admin', 'manager'])
    def create(self, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                product_type = self._product_type_repo.get_by_id(
                    data['product_type_id'],
                    session=s
                )
                feature_values = self._feature_value_repo.filter_by_ids(
                    data['feature_values'],
                    session=s
                )

                if not self._feature_values_policy.are_allowed_if_product_type_is(
                    feature_values,
                    product_type
                ):
                    raise self.FeatureValuesInvalid()

                if data.get('upc') is not None and self._repo.get_first_by_upc(data['upc']) is not None:
                    raise self.SameUPC()


                return self._repo.add_product(
                    data['price'],
                    data['discount'],
                    data['quantity'],
                    data.get('upc'),
                    data['images'],
                    product_type,
                    feature_values,
                    session=s
                )
        except self._feature_value_repo.DoesNotExist:
            raise self.FeatureValuesInvalid()
        except self._product_type_repo.DoesNotExist:
            raise self.ProductTypeInvalid()

    @allow_roles(['admin', 'manager'])
    def update(self, id_, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                product_type = self._product_type_repo.get_by_id(
                    data['product_type_id'],
                    session=s
                )
                feature_values = self._feature_value_repo.filter_by_ids(
                    data['feature_values'],
                    session=s
                )

                if not self._feature_values_policy.are_allowed_if_product_type_is(
                    feature_values,
                    product_type
                ):
                    raise self.FeatureValuesInvalid()

                if data.get('upc') is not None:
                    product_with_same_upc = self._repo.get_first_by_upc(data['upc'])
                    if product_with_same_upc and product_with_same_upc.id != id_:
                        raise self.SameUPC()

                return self._repo.update_product(
                    id_,
                    data['price'],
                    data['discount'],
                    data['quantity'],
                    data.get('upc'),
                    data['images'],
                    product_type,
                    feature_values,
                    session=s
                )
        except self._feature_value_repo.DoesNotExist:
            raise self.FeatureValuesInvalid()
        except self._product_type_repo.DoesNotExist:
            raise self.ProductTypeInvalid()

    def get_all(self, offset=None, limit=None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_by_ids(self, ids):
        return self._repo.filter_by_ids(ids)

    def get_for_product_type(self, product_type_id):
        return self._repo.get_for_product_type(product_type_id)

    def get_one(self, id_):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.ProductNotFound()

    @allow_roles(['admin', 'manager'])
    def delete(self, id_, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.ProductNotFound()

    class ProductNotFound(Exception):
        pass

    class FeatureValuesInvalid(Exception):
        pass

    class ProductTypeInvalid(Exception):
        pass
    
    class SameUPC(Exception):
        pass
