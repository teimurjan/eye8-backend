from typing import Dict, List
from sqlalchemy.orm.session import Session as SQLAlchemySession
from src.repos.base import Repo, with_session, set_intl_texts
from src.models import Characteristic, CharacteristicValue, CharacteristicValueName


class CharacteristicValueRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, CharacteristicValue)

    @with_session
    def add_characteristic_value(
        self, names: Dict, characteristic: Characteristic, session: SQLAlchemySession
    ) -> CharacteristicValue:
        characteristic_value = CharacteristicValue()

        set_intl_texts(
            names,
            characteristic_value,
            "names",
            CharacteristicValueName,
            session=session,
        )

        characteristic_value.characteristic_id = characteristic.id

        session.add(characteristic_value)
        session.flush()

        characteristic_value.names
        characteristic_value.characteristic
        characteristic_value.created_on
        characteristic_value.updated_on

        return characteristic_value

    @with_session
    def update_characteristic_value(
        self,
        id_: int,
        names: Dict,
        characteristic: Characteristic,
        session: SQLAlchemySession = None,
    ) -> CharacteristicValue:
        characteristic_value = self.get_by_id(id_, session=session)

        set_intl_texts(
            names,
            characteristic_value,
            "names",
            CharacteristicValueName,
            session=session,
        )

        characteristic_value.characteristic_id = characteristic.id

        session.flush()

        characteristic_value.created_on
        characteristic_value.updated_on

        return characteristic_value

    @with_session
    def get_all_by_characteristic(
        self,
        characteristic_id: int,
        offset: int = None,
        limit: int = None,
        session: SQLAlchemySession = None,
    ) -> List[CharacteristicValue]:
        return (
            self.get_query(session=session)
            .filter(Characteristic.id == characteristic_id)
            .order_by(CharacteristicValue.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    class DoesNotExist(Exception):
        pass
