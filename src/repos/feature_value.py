from src.repos.base import Repo, with_session, set_intl_texts
from src.models import FeatureValue, FeatureValueName, FeatureType


class FeatureValueRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, FeatureValue)

    @with_session
    def add_feature_value(self, names, feature_type, session):
        feature_value = FeatureValue()

        set_intl_texts(names, feature_value, 'names', FeatureValueName, session=session)

        feature_value.feature_type_id = feature_type.id

        session.add(feature_value)

        session.flush()

        feature_value.names
        feature_value.feature_type

        return feature_value

    @with_session
    def update_feature_value(self, id_, names, feature_type, session):
        feature_value = self.get_by_id(id_, session=session)
        
        set_intl_texts(names, feature_value, 'names', FeatureValueName, session=session)

        feature_value.feature_type_id = feature_type.id

        return feature_value

    class DoesNotExist(Exception):
        pass