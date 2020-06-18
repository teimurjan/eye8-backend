from itertools import groupby
from operator import itemgetter

import bcrypt
from sqlalchemy import desc, select
from sqlalchemy.orm import defaultload, joinedload

from src.models import Order, OrderItem, PromoCode
from src.models.order import order_item
from src.models.product import Product
from src.models.product_type import ProductType
from src.models.product_type.name import ProductTypeName
from src.models.promo_code import ProductXPromoCodeTable
from src.repos.base import NonDeletableRepo, with_session
from src.utils.array import find_in_array


class OrderRepo(NonDeletableRepo):
    def __init__(self, db_conn):
        super().__init__(db_conn, Order)

    @with_session
    def get_for_user(self, user_id, offset=None, limit=None, session=None):
        q = (
            self
            .get_non_deleted_query(session=session)
            .filter(Order.user_id == user_id)
        )
        orders = (
            q
            .order_by(desc(Order.id))
            .offset(offset)
            .limit(limit)
            .options(joinedload(Order.items))
            .all()
        )
        orders_count = q.count()

        promo_codes = (
            session
            .query(PromoCode)
            .filter(PromoCode.id.in_({
                order.promo_code.id for order in orders if order.promo_code
            }))
            .options(joinedload(PromoCode.products))
            .all()
        )
        for order in orders:
            if order.promo_code:
                _, promo_code = find_in_array(
                    promo_codes, lambda promo_code: promo_code.id == order.promo_code.id
                )
                if promo_code:
                    order.promo_code = promo_code

        return orders, orders_count

    @with_session
    def get_by_id(self, id_, session) -> Order:
        objects = (
            self
            .get_non_deleted_query(session=session)
            .options(joinedload(Order.items))
            .filter(Order.id == id_)
            .all()
        )
        if len(objects) == 0:
            raise self.DoesNotExist()

        return objects[0]

    @with_session
    def add_order(self, user, user_name, user_phone_number, user_address, items, promo_code, session):
        order = Order()
        order.user = user
        order.user_name = user_name
        order.user_phone_number = user_phone_number
        order.user_address = user_address
        order.promo_code = promo_code
        order.promo_code_discount = promo_code.discount if promo_code else None
        order.promo_code_value = promo_code.value if promo_code else None

        order_items = []
        for item in items:
            order_item = OrderItem()
            order_item.product = item['product']
            order_item.product_price_per_item = item['product'].price
            order_item.product_discount = item['product'].discount
            order_item.quantity = item['quantity']
            order_items.append(order_item)

        order.items = order_items

        session.add(order)
        session.flush()

        order.created_on
        order.updated_on

        return order

    @with_session
    def update_order(self, id_, user_name, user_phone_number, user_address, items, status, promo_code, session):
        order = self.get_by_id(id_, session=session)
        order.user_name = user_name
        order.user_phone_number = user_phone_number
        order.user_address = user_address
        order.status = status
        order.promo_code = promo_code
        order.promo_code_discount = promo_code.discount if promo_code else None
        order.promo_code_value = promo_code.value if promo_code else None

        new_order_items = []
        for item in items:
            order_item = OrderItem()
            order_item.product = item['product']
            order_item.product_price_per_item = item['product'].price
            order_item.product_discount = item['product'].discount
            order_item.quantity = item['quantity']
            new_order_items.append(order_item)

        order.items = new_order_items

        session.flush()

        order.created_on
        order.updated_on

        return order

    @with_session
    def has_for_date_range(self, start_date, end_date=None, session=None):
        q = (
            self
            .get_non_deleted_query(session=session)
            .filter(Order.created_on >= start_date)
        )

        if end_date is not None:
            q = q.filter(Order.created_on < end_date)

        return q.count() > 0

    @with_session
    def has_with_promo_code(self, promo_code_id, session=None):
        q = (
            self
            .get_non_deleted_query(session=session)
            .filter(Order.promo_code_id == promo_code_id)
        )

        return q.count() > 0

    class DoesNotExist(Exception):
        pass
