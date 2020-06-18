from src.repos.base import Repo, with_session
from src.models import Language


class LanguageRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, Language)

    @with_session
    def filter_by_name(self, name: str, session):
        return self.get_query(session=session).filter(Language.name == name).all()

    class DoesNotExist(Exception):
        pass