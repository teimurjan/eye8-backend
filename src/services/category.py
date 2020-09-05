from src.validation_rules.category.create import CreateCategoryData
from src.validation_rules.category.update import UpdateCategoryData


from src.repos.category import CategoryRepo
from src.repos.product_type import ProductTypeRepo
from src.services.decorators import allow_roles


class CategoryService:
    def __init__(self, repo: CategoryRepo, product_type_repo: ProductTypeRepo):
        self._repo = repo
        self._product_type_repo = product_type_repo

    def get_all(self):
        return self._repo.get_all()

    def get_one(self, id_: int):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    def get_one_by_slug(self, slug: str):
        category = self._repo.get_by_slug(slug)
        if category is None:
            raise self.CategoryNotFound()

        return category

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateCategoryData, *args, **kwargs):
        with self._repo.session() as s:
            category = self._repo.add_category(
                data["names"], data.get("parent_category_id"), session=s
            )

            return category

    @allow_roles(["admin", "manager"])
    def update(self, id_: int, data: UpdateCategoryData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                parent_category_id = data.get("parent_category_id")
                if parent_category_id != None and parent_category_id == id_:
                    raise self.CircularCategoryConnection()

                category = self._repo.update_category(
                    id_, data["names"], parent_category_id, session=s
                )

                return category
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            with self._repo.session() as s:
                if self._repo.has_children(id_, session=s):
                    raise self.CategoryWithChildrenIsUntouchable()

                if self._product_type_repo.has_with_category(id_, session=s):
                    raise self.CategoryWithProductTypesIsUntouchable()

                self._repo.delete(id_, session=s)
        except self._repo.DoesNotExist:
            raise self.CategoryNotFound()

    def search(self, query: str):
        return self._repo.search(query)

    class CategoryNotFound(Exception):
        pass

    class CircularCategoryConnection(Exception):
        pass

    class CategoryWithChildrenIsUntouchable(Exception):
        pass

    class CategoryWithProductTypesIsUntouchable(Exception):
        pass
