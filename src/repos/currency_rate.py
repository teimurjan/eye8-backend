from datetime import timedelta

from src.models import CurrencyRate
from src.repos.base import Repo, with_session


class CurrencyRateRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, CurrencyRate)

    @with_session
    def exists_for_date(self, name, date, session):
        return self.get_query(session=session).filter(CurrencyRate.name == name).filter(CurrencyRate.created_on+timedelta(days=1) > date).order_by(CurrencyRate.id).count() > 0

    @with_session
    def add_currency_rate(self, name: str, value: int, session):
        currency_rate = CurrencyRate()
        currency_rate.name = name
        currency_rate.value = value

        session.add(currency_rate)
        session.flush()

        currency_rate.created_on
        currency_rate.updated_on


        return currency_rate

    @with_session
    def filter_by_name(self, name: str, session):
        return self.get_query(session=session).filter(CurrencyRate.name == name).order_by(CurrencyRate.id).all()

    class DoesNotExist(Exception):
        pass
