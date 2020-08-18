from src.validation_rules.feature_type.create import CreateFeatureTypeData
from src.validation_rules.feature_type.update import UpdateFeatureTypeData
from src.services.decorators import allow_roles
from src.repos.feature_type import FeatureTypeRepo


class FeatureTypeService:
    def __init__(self, repo: FeatureTypeRepo):
        self._repo = repo

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateFeatureTypeData, *args, **kwargs):
        feature_type = self._repo.add_feature_type(data["names"])
        return feature_type

    @allow_roles(["admin", "manager"])
    def update(
        self, feature_type_id: int, data: UpdateFeatureTypeData, *args, **kwargs
    ):
        return self._repo.update_feature_type(feature_type_id, data["names"])

    def get_all(self, offset: int = None, limit: int = None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_one(self, id_: int):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.FeatureTypeNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.FeatureTypeNotFound()

    class FeatureTypeNotFound(Exception):
        pass
