from typing import Dict
from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import Repo, with_session
from src.models import FeatureType, Category


class FeatureTypeRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, FeatureType)

    @with_session
    def add_feature_type(self, names: Dict, session: SQLAlchemySession = None):
        feature_type = FeatureType()

        feature_type.name_en = names["en"]
        feature_type.name_ru = names["ru"]

        session.add(feature_type)
        session.flush()

        feature_type.created_on
        feature_type.updated_on

        return feature_type

    @with_session
    def update_feature_type(
        self, id_: int, names: Dict, session: SQLAlchemySession = None
    ):
        feature_type = self.get_by_id(id_, session=session)

        feature_type.name_en = names["en"]
        feature_type.name_ru = names["ru"]

        session.flush()

        feature_type.created_on
        feature_type.updated_on

        return feature_type

    @with_session
    def filter_by_category(self, category: Category, session: SQLAlchemySession = None):
        return (
            self.get_query(session=session)
            .filter(FeatureType.categories.any(Category.id == category.id))
            .all()
        )

    class DoesNotExist(Exception):
        pass
