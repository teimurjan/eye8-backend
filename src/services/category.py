import json

from elasticsearch.client import Elasticsearch

from src.models.intl import Language
from src.repos.category import CategoryRepo
from src.repos.product_type import ProductTypeRepo
from src.services.decorators import allow_roles


class CategoryService:
    def __init__(self, repo: CategoryRepo, product_type_repo: ProductTypeRepo, es: Elasticsearch):
        self._repo = repo
        self._product_type_repo = product_type_repo
        self._es = es

    def get_all(self):
        return self._repo.get_all()

    def get_one(self, id_):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    def get_one_by_slug(self, slug):
        category = self._repo.get_by_slug(slug)
        if category is None:
            raise self.CategoryNotFound()

        return category

    @allow_roles(['admin', 'manager'])
    def create(self, data, *args, **kwargs):
        with self._repo.session() as s:
            category = self._repo.add_category(
                data['names'],
                data.get('parent_category_id'),
                session=s
            )
            self.set_to_search_index(category)

            return category

    @allow_roles(['admin', 'manager'])
    def update(self, id_, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                parent_category_id = data.get('parent_category_id')
                if (parent_category_id != None and parent_category_id == id_):
                    raise self.CircularCategoryConnection()

                category = self._repo.update_category(
                    id_,
                    data['names'],
                    parent_category_id,
                    session=s
                )

                self.set_to_search_index(category)

                return category
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    @allow_roles(['admin', 'manager'])
    def delete(self, id_, *args, **kwargs):
        try:
            with self._repo.session() as s:
                if self._repo.has_children(id_, session=s):
                    raise self.CategoryWithChildrenIsUntouchable()

                if self._product_type_repo.has_with_category(id_, session=s):
                    raise self.CategoryWithProductTypesIsUntouchable()

                self._repo.delete(id_, session=s)
                self.remove_from_search_index(id_)
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    def set_to_search_index(self, category):
        body = {}
        for name in category.names:
            body[name.language.name] = name.value
        self._es.index(index='category', id=category.id, body=body)

    def remove_from_search_index(self, id_):
        self._es.delete(index='category', id=id_)

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
        result = self._es.search(index='category', body=body)

        ids = [hit['_id'] for hit in result['hits']['hits']]

        return self._repo.filter_by_ids(ids)

    class CategoryNotFound(Exception):
        pass

    class CircularCategoryConnection(Exception):
        pass

    class CategoryWithChildrenIsUntouchable(Exception):
        pass

    class CategoryWithProductTypesIsUntouchable(Exception):
        pass
