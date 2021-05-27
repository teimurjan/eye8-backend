from typing import Dict
from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import Repo, with_session
from src.models import Characteristic


class CharacteristicRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, Characteristic)

    @with_session
    def add_characteristic(self, names: Dict, session: SQLAlchemySession = None):
        characteristic = Characteristic()

        characteristic.name_en = names["en"]
        characteristic.name_ru = names["ru"]

        session.add(characteristic)
        session.flush()

        characteristic.created_on
        characteristic.updated_on

        return characteristic

    @with_session
    def update_characteristic(
        self, id_: int, names: Dict, session: SQLAlchemySession = None
    ):
        characteristic = self.get_by_id(id_, session=session)

        characteristic.name_en = names["en"]
        characteristic.name_ru = names["ru"]

        session.flush()

        characteristic.created_on
        characteristic.updated_on

        return characteristic

    class DoesNotExist(Exception):
        pass
