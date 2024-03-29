from src.models.feature_type import FeatureType
from typing import Dict
from sqlalchemy.orm.session import Session as SQLAlchemySession
from src.repos.base import Repo, with_session
from src.models import FeatureValue


class FeatureValueRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, FeatureValue)

    @with_session
    def add_feature_value(
        self, names: Dict, feature_type: FeatureType, session: SQLAlchemySession,
    ):
        feature_value = FeatureValue()

        feature_value.name_en = names["en"]
        feature_value.name_ru = names["ru"]

        feature_value.feature_type_id = feature_type.id

        session.add(feature_value)
        session.flush()

        feature_value.feature_type
        feature_value.created_on
        feature_value.updated_on

        return feature_value

    @with_session
    def update_feature_value(
        self,
        id_: int,
        names: Dict,
        feature_type: FeatureType,
        session: SQLAlchemySession = None,
    ):
        feature_value = self.get_by_id(id_, session=session)

        feature_value.name_en = names["en"]
        feature_value.name_ru = names["ru"]

        feature_value.feature_type_id = feature_type.id

        session.flush()

        feature_value.created_on
        feature_value.updated_on

        return feature_value

    class DoesNotExist(Exception):
        pass
