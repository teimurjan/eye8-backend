from src.repos.characteristic_value import CharacteristicValueRepo
from src.validation_rules.product_type.create import CreateProductTypeData
from src.validation_rules.product_type.update import UpdateProductTypeData

from src.repos.category import CategoryRepo
from src.repos.feature_type import FeatureTypeRepo
from src.repos.product import ProductRepo
from src.repos.product_type import ProductTypeRepo
from src.services.decorators import allow_roles
from src.utils.sorting import ProductTypeSortingType


class ProductTypeService:
    def __init__(
        self,
        repo: ProductTypeRepo,
        category_repo: CategoryRepo,
        feature_type_repo: FeatureTypeRepo,
        product_repo: ProductRepo,
        characteristic_value_repo: CharacteristicValueRepo,
    ):
        self._repo = repo
        self._category_repo = category_repo
        self._feature_type_repo = feature_type_repo
        self._product_repo = product_repo
        self._characteristic_value_repo = characteristic_value_repo

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateProductTypeData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                categories = self._category_repo.filter_by_ids(
                    data["categories"], session=s
                )

                feature_types = self._feature_type_repo.filter_by_ids(
                    data["feature_types"], session=s
                )
                if len(feature_types) != len(data["feature_types"]):
                    raise self.FeatureTypesInvalid()

                characteristic_values = self._characteristic_value_repo.filter_by_ids(
                    data["characteristic_values"], session=s
                )
                if len(characteristic_values) != len(data["characteristic_values"]):
                    raise self.CharacteristicValuesInvalid()

                product_type = self._repo.add_product_type(
                    data["names"],
                    data["descriptions"],
                    data["short_descriptions"],
                    data["instagram_links"],
                    data["image"],
                    categories,
                    feature_types,
                    characteristic_values,
                    session=s,
                )

                return product_type
        except self._category_repo.DoesNotExist:
            raise self.CategoryInvalid()
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypesInvalid()

    @allow_roles(["admin", "manager"])
    def update(self, id_: int, data: UpdateProductTypeData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                categories = self._category_repo.filter_by_ids(
                    data["categories"], session=s
                )

                feature_types = self._feature_type_repo.filter_by_ids(
                    data["feature_types"], session=s
                )
                if len(feature_types) != len(data["feature_types"]):
                    raise self.FeatureTypesInvalid()

                characteristic_values = self._characteristic_value_repo.filter_by_ids(
                    data["characteristic_values"], session=s
                )
                if len(characteristic_values) != len(data["characteristic_values"]):
                    raise self.CharacteristicValuesInvalid()

                product_type = self._repo.update_product_type(
                    id_,
                    data["names"],
                    data["descriptions"],
                    data["short_descriptions"],
                    data["instagram_links"],
                    data["image"],
                    categories,
                    feature_types,
                    characteristic_values,
                    session=s,
                )

                return product_type
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()
        except self._category_repo.DoesNotExist:
            raise self.CategoryInvalid()
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypesInvalid()

    def get_all(
        self,
        available: bool = False,
        sorting_type: ProductTypeSortingType = None,
        offset: int = None,
        limit: int = None,
    ):
        return self._repo.get_all(
            available=available, offset=offset, limit=limit, sorting_type=sorting_type,
        )

    def get_all_by_category(
        self,
        category_slug: str,
        sorting_type: ProductTypeSortingType,
        available: bool = False,
        offset: int = None,
        limit: int = None,
    ):
        with self._repo.session() as s:
            category = self._category_repo.get_by_slug(category_slug, session=s)
            children_categories = self._category_repo.get_children(
                category.id, session=s
            )
            category_ids = [category.id for category in children_categories]
            product_types, count = self._repo.get_all(
                available=available,
                category_ids=category_ids,
                sorting_type=sorting_type,
                offset=offset,
                limit=limit,
                session=s,
            )
            return product_types, count

    def get_one(self, id_: int):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()

    def get_one_by_slug(self, slug):
        product_type = self._repo.get_by_slug(slug)
        if product_type is None:
            raise self.ProductTypeNotFound()

        return product_type

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            if self._product_repo.has_with_product_type(id_):
                raise self.ProductTypeWithProductsIsUntouchable()

            self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()

    def search(
        self, query: str, available: bool = False,
    ):
        return self._repo.search(query, available)

    class ProductTypeNotFound(Exception):
        pass

    class CategoryInvalid(Exception):
        pass

    class FeatureTypesInvalid(Exception):
        pass

    class CharacteristicValuesInvalid(Exception):
        pass

    class ProductTypeWithProductsIsUntouchable(Exception):
        pass
