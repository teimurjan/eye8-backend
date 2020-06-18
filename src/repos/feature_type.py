from src.repos.base import Repo, set_intl_texts, with_session
from src.models import FeatureType, FeatureTypeName, Category


class FeatureTypeRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, FeatureType)

    @with_session
    def add_feature_type(self, names, session):
        feature_type = FeatureType()

        set_intl_texts(names, feature_type, 'names',
                       FeatureTypeName, session=session)

        session.add(feature_type)

        feature_type.names
        feature_type.created_on
        feature_type.updated_on

        session.flush()

        return feature_type

    @with_session
    def update_feature_type(self, id_, names, session):
        feature_type = self.get_by_id(id_, session=session)

        set_intl_texts(names, feature_type, 'names',
                       FeatureTypeName, session=session)

        return feature_type

    @with_session
    def filter_by_category(self, category, session):
        return (
            self
            .get_query(session=session)
            .filter(FeatureType.categories.any(Category.id == category.id))
            .all()
        )

    class DoesNotExist(Exception):
        pass
