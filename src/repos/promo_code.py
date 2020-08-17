from typing import List, Optional
from sqlalchemy.orm.session import Session as SQLAlchemySession


from src.models import PromoCode, Product
from src.repos.base import NonDeletableRepo, with_session


class PromoCodeRepo(NonDeletableRepo):
    def __init__(self, db_conn):
        super().__init__(db_conn, PromoCode)

    @with_session
    def add_promo_code(
        self,
        value: str,
        discount: int,
        amount: Optional[int],
        is_active: bool,
        disable_on_use: bool,
        products: List[Product],
        session: SQLAlchemySession,
    ):
        if self.is_value_used(value):
            raise self.ValueNotUnique()

        promo_code = PromoCode()
        promo_code.value = value
        promo_code.discount = discount
        promo_code.amount = amount
        promo_code.is_active = is_active
        promo_code.disable_on_use = disable_on_use
        promo_code.products = products

        session.add(promo_code)
        session.flush()

        promo_code.created_on
        promo_code.updated_on

        return promo_code

    @with_session
    def update_promo_code(
        self,
        id_: int,
        is_active: bool,
        disable_on_use: bool,
        products: List[Product],
        session: SQLAlchemySession,
    ):
        promo_code = self.get_by_id(id_, session=session)

        promo_code.is_active = is_active
        promo_code.disable_on_use = disable_on_use
        promo_code.products = products

        session.flush()

        promo_code.created_on
        promo_code.updated_on

        return promo_code

    @with_session
    def is_value_used(self, value: str, session: SQLAlchemySession):
        return (
            self.get_query(session=session).filter(PromoCode.value == value).count() > 0
        )

    @with_session
    def get_by_value(self, value: str, session: SQLAlchemySession):
        q = self.get_non_deleted_query(session=session).filter(PromoCode.value == value)
        count = q.count()
        if count == 0:
            raise self.DoesNotExist()

        return q.first()

    class DoesNotExist(Exception):
        pass

    class ValueNotUnique(Exception):
        pass
