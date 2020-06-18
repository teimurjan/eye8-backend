import json

from elasticsearch.client import Elasticsearch

from src.models.intl import Language
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
        es: Elasticsearch
    ):
        self._repo = repo
        self._category_repo = category_repo
        self._feature_type_repo = feature_type_repo
        self._product_repo = product_repo
        self._es = es

    @allow_roles(['admin', 'manager'])
    def create(self, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                category = self._category_repo.get_by_id(
                    data['category_id'],
                    session=s
                )

                feature_types = self._feature_type_repo.filter_by_ids(
                    data['feature_types'],
                    session=s
                )

                if len(feature_types) != len(data['feature_types']):
                    raise self.FeatureTypesInvalid()

                product_type = self._repo.add_product_type(
                    data['names'],
                    data['descriptions'],
                    data['short_descriptions'],
                    data['image'],
                    category,
                    feature_types,
                    session=s
                )

                self.set_to_search_index(product_type)

                return product_type
        except self._category_repo.DoesNotExist:
            raise self.CategoryInvalid()
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypesInvalid()

    @allow_roles(['admin', 'manager'])
    def update(self, id_, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                category = self._category_repo.get_by_id(
                    data['category_id'],
                    session=s
                )

                feature_types = self._feature_type_repo.filter_by_ids(
                    data['feature_types'],
                    session=s
                )

                if len(feature_types) != len(data['feature_types']):
                    raise self.FeatureTypesInvalid()

                product_type = self._repo.update_product_type(
                    id_,
                    data['names'],
                    data['descriptions'],
                    data['short_descriptions'],
                    data['image'],
                    category,
                    feature_types,
                    session=s
                )

                self.set_to_search_index(product_type)

                return product_type
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()
        except self._category_repo.DoesNotExist:
            raise self.CategoryInvalid()
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypesInvalid()

    def get_all(
        self,
        join_products: bool = False,
        only_available: bool = True,
        sorting_type: ProductTypeSortingType = None,
        offset: int=None,
        limit: int=None,
    ):
        return self._repo.get_all(
            join_products=join_products,
            only_available=only_available,
            offset=offset,
            limit=limit,
            sorting_type=sorting_type
        )

    def get_all_by_category(self, category_slug: str, sorting_type: ProductTypeSortingType, offset: int = None, limit: int = None):
        with self._repo.session() as s:
            category = self._category_repo.get_by_slug(
                category_slug, session=s)
            children_categories = self._category_repo.get_children(
                category.id, session=s)
            categories_ids = [category.id for category in children_categories]
            product_types, count = self._repo.get_all(
                categories_ids,
                sorting_type,
                offset,
                limit,
                join_products=True,
                session=s
            )
            return product_types, count

    def get_one(self, id_):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()

    def get_one_by_slug(self, slug):
        product_type = self._repo.get_by_slug(slug)
        if product_type is None:
            raise self.ProductTypeNotFound()

        return product_type

    @allow_roles(['admin', 'manager'])
    def delete(self, id_, *args, **kwargs):
        try:
            if self._product_repo.has_with_product_type(id_):
                raise self.ProductTypeWithProductsIsUntouchable()

            self._repo.delete(id_)
            self.remove_from_search_index(id_)
        except self._repo.DoesNotExist:
            raise self.ProductTypeNotFound()

    def set_to_search_index(self, product_type):
        body = {}
        for name in product_type.names:
            body[name.language.name] = name.value
        self._es.index(index='product_type', id=product_type.id, body=body)

    def remove_from_search_index(self, id_):
        self._es.delete(index='product_type', id=id_)

    def search(self, query: str, language: Language):
        formatted_query = query.lower()
        body = json.loads('''
            {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "prefix": {
                                    "%s": "%s"
                                }
                            },
                            {
                                "match": {
                                    "%s": {
                                        "query": "%s",
                                        "fuzziness": "AUTO",
                                        "operator": "and"
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        ''' % (language.name, formatted_query, language.name, formatted_query)
        )
        result = self._es.search(index='product_type', body=body)

        ids = [hit['_id'] for hit in result['hits']['hits']]

        return self._repo.filter_by_ids(ids)

    class ProductTypeNotFound(Exception):
        pass

    class CategoryInvalid(Exception):
        pass

    class FeatureTypesInvalid(Exception):
        pass

    class ProductTypeWithProductsIsUntouchable(Exception):
        pass
