from src.services.decorators import allow_roles
from src.repos.feature_value import FeatureValueRepo
from src.repos.feature_type import FeatureTypeRepo


class FeatureValueService:
    def __init__(self, repo: FeatureValueRepo, feature_type_repo: FeatureTypeRepo):
        self._repo = repo
        self._feature_type_repo = feature_type_repo

    @allow_roles(['admin', 'manager'])
    def create(self, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                feature_type = self._feature_type_repo.get_by_id(
                    data['feature_type_id'],
                    session=s
                )

                feature_value = self._repo.add_feature_value(
                    data['names'],
                    feature_type,
                    session=s
                )

                return feature_value
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypeInvalid()

    @allow_roles(['admin', 'manager'])
    def update(self, id_, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                feature_type = self._feature_type_repo.get_by_id(
                    data['feature_type_id'],
                    session=s
                )

                return self._repo.update_feature_value(
                    id_,
                    data['names'],
                    feature_type=feature_type,
                    session=s
                )
        except self._feature_type_repo.DoesNotExist:
            raise self.FeatureTypeInvalid()

    def get_all(self, offset=None, limit=None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_one(self, id_):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.FeatureValueNotFound()

    @allow_roles(['admin', 'manager'])
    def delete(self, id_, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.FeatureValueNotFound()

    class FeatureValueNotFound(Exception):
        pass

    class FeatureTypeInvalid(Exception):
        pass

