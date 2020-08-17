from typing import Dict

from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import Repo, set_intl_texts, with_session
from src.models import FeatureType, FeatureTypeName, Category


class FeatureTypeRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, FeatureType)

    @with_session
    def add_feature_type(self, names: Dict, session: SQLAlchemySession):
        feature_type = FeatureType()

        set_intl_texts(names, feature_type, "names", FeatureTypeName, session=session)

        session.add(feature_type)
        session.flush()

        feature_type.names
        feature_type.created_on
        feature_type.updated_on

        return feature_type

    @with_session
    def update_feature_type(self, id_: int, names: Dict, session: SQLAlchemySession):
        feature_type = self.get_by_id(id_, session=session)

        set_intl_texts(names, feature_type, "names", FeatureTypeName, session=session)

        session.flush()

        feature_type.created_on
        feature_type.updated_on

        return feature_type

    @with_session
    def filter_by_category(self, category: Category, session: SQLAlchemySession):
        return (
            self.get_query(session=session)
            .filter(FeatureType.categories.any(Category.id == category.id))
            .all()
        )

    class DoesNotExist(Exception):
        pass
