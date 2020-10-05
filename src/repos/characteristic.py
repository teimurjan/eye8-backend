from typing import Dict

from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import Repo, set_intl_texts, with_session
from src.models import Characteristic, CharacteristicName


class CharacteristicRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, Characteristic)

    @with_session
    def add_characteristic(self, names: Dict, session: SQLAlchemySession = None):
        characteristic = Characteristic()

        set_intl_texts(
            names, characteristic, "names", CharacteristicName, session=session
        )

        session.add(characteristic)
        session.flush()

        characteristic.names
        characteristic.created_on
        characteristic.updated_on

        return characteristic

    @with_session
    def update_characteristic(
        self, id_: int, names: Dict, session: SQLAlchemySession = None
    ):
        characteristic = self.get_by_id(id_, session=session)

        set_intl_texts(
            names, characteristic, "names", CharacteristicName, session=session
        )

        session.flush()

        characteristic.created_on
        characteristic.updated_on

        return characteristic

    class DoesNotExist(Exception):
        pass
