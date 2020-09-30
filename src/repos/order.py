from datetime import datetime
from src.validation_rules.order.create import OrderItemData
from typing import Any, Dict, List

from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy.sql.expression import desc

from src.models import Order, OrderItem, User, PromoCode
from src.repos.base import NonDeletableRepo, with_session


class OrderRepo(NonDeletableRepo):
    def __init__(self, db_engine):
        super().__init__(db_engine, Order)

    @with_session
    def get_for_user(
        self,
        user_id: int,
        offset: int = None,
        limit: int = None,
        session: SQLAlchemySession = None,
    ):
        q = self.get_non_deleted_query(session=session).filter(Order.user_id == user_id)
        orders = q.order_by(desc(Order.id)).offset(offset).limit(limit).all()

        return orders, q.count()

    @with_session
    def get_by_id(self, id_: int, session: SQLAlchemySession = None) -> Order:
        orders = (
            self.get_non_deleted_query(session=session).filter(Order.id == id_).all()
        )
        if len(orders) == 0:
            raise self.DoesNotExist()

        return orders[0]

    @with_session
    def add_order(
        self,
        user: User,
        user_name: str,
        user_phone_number: str,
        user_address: str,
        items: List[OrderItemData],
        promo_code: PromoCode,
        session: SQLAlchemySession = None,
    ):
        order = Order()
        order.user = user
        order.user_name = user_name
        order.user_phone_number = user_phone_number
        order.user_address = user_address
        order.promo_code_value = promo_code.value
        order.promo_code_discount = promo_code.discount
        order.promo_code_amount = promo_code.amount
        order.promo_code_products_ids = promo_code.products_ids

        order_items = []
        for item in items:
            order_item = OrderItem()
            order_item.product = item["product"]
            order_item.product_price_per_item = item["product"].price
            order_item.product_discount = item["product"].discount
            order_item.quantity = item["quantity"]
            order_items.append(order_item)

        order.items = order_items

        session.add(order)
        session.flush()

        order.created_on
        order.updated_on

        return order

    @with_session
    def update_order(
        self,
        id_: int,
        user_name: str,
        user_phone_number: str,
        user_address: str,
        items: List[Dict[str, Any]],
        status: str,
        promo_code: PromoCode,
        session: SQLAlchemySession = None,
    ):
        order = self.get_by_id(id_, session=session)
        order.user_name = user_name
        order.user_phone_number = user_phone_number
        order.user_address = user_address
        order.status = status
        order.promo_code = promo_code

        new_order_items = []
        for item in items:
            order_item = OrderItem()
            order_item.product = item["product"]
            order_item.product_price_per_item = item["product"].price
            order_item.product_discount = item["product"].discount
            order_item.quantity = item["quantity"]
            new_order_items.append(order_item)

        order.items = new_order_items

        session.flush()

        order.created_on
        order.updated_on

        return order

    @with_session
    def has_for_date_range(
        self,
        start_date: datetime,
        end_date: datetime = None,
        session: SQLAlchemySession = None,
    ):
        q = self.get_non_deleted_query(session=session).filter(
            Order.created_on >= start_date
        )

        if end_date is not None:
            q = q.filter(Order.created_on < end_date)

        return q.count() > 0

    class DoesNotExist(Exception):
        pass
