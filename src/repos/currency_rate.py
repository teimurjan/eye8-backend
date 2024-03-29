from datetime import datetime, timedelta
from typing import cast
from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.models import CurrencyRate
from src.repos.base import Repo, with_session


class CurrencyRateRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, CurrencyRate)

    @with_session
    def exists_for_date(
        self, name: str, date: datetime, session: SQLAlchemySession = None
    ):
        before_date = cast(datetime, CurrencyRate.created_on) + timedelta(days=1)
        return (
            self.get_query(session=session)
            .filter(CurrencyRate.name == name)
            .filter(before_date > date)
            .order_by(CurrencyRate.id)
            .count()
            > 0
        )

    @with_session
    def add_currency_rate(
        self, name: str, value: int, session: SQLAlchemySession = None
    ):
        currency_rate = CurrencyRate()
        currency_rate.name = name
        currency_rate.value = value

        session.add(currency_rate)
        session.flush()

        currency_rate.created_on
        currency_rate.updated_on

        return currency_rate

    @with_session
    def filter_by_name(self, name: str, session: SQLAlchemySession = None):
        return (
            self.get_query(session=session)
            .filter(CurrencyRate.name == name)
            .order_by(CurrencyRate.id)
            .all()
        )

    class DoesNotExist(Exception):
        pass
