from src.validation_rules.order.update import UpdateOrderData
from src.validation_rules.order.create import CreateOrderData
from src.models.user import User
from typing import Optional
from flask import current_app as app
from flask import render_template

from src.errors import InvalidEntityFormat
from src.mail import Mail
from src.repos.order import OrderRepo
from src.repos.product import ProductRepo
from src.repos.promo_code import PromoCodeRepo
from src.services.decorators import allow_roles


class OrderService:
    def __init__(
        self,
        repo: OrderRepo,
        product_repo: ProductRepo,
        promo_code_repo: PromoCodeRepo,
        mail: Mail,
    ):
        self._repo = repo
        self._product_repo = product_repo
        self._promo_code_repo = promo_code_repo
        self._mail = mail

    def create(self, data: CreateOrderData, user: Optional[User]):
        try:
            with self._repo.session() as s:
                for item in data["items"]:
                    product = self._product_repo.get_by_id(
                        item["product_id"], session=s
                    )
                    item["product"] = product

                promo_code_value = data.get("promo_code")
                promo_code = None

                if promo_code_value:
                    promo_code = self._promo_code_repo.get_by_value(
                        promo_code_value.lower(), session=s
                    )

                    if not promo_code.is_active:
                        raise self.PromoCodeInvalid()

                    if promo_code.disable_on_use:
                        promo_code.is_active = False

                order = self._repo.add_order(
                    user,
                    data["user_name"],
                    data["user_phone_number"],
                    data["user_address"],
                    data["items"],
                    promo_code,
                    session=s,
                )

                link = app.config.get("HOST") + "/admin/orders/" + str(order.id)
                title = "Заказ!"
                description = (
                    "Имя: "
                    + order.user_name
                    + "<br/>"
                    + "Телефон: "
                    + order.user_phone_number
                    + "<br/>"
                    + "Адрес: "
                    + order.user_address
                )
                link_text = "Подробнее"
                subject = link_text
                body = render_template(
                    "link_email.html",
                    link=link,
                    title=title,
                    description=description,
                    link_text=link_text,
                    preheader=title,
                )

                self._mail.send(subject, body, [app.config.get("MAIL_ORDERS_USERNAME")])

                return order
        except self._promo_code_repo.DoesNotExist:
            raise self.PromoCodeInvalid()
        except self._product_repo.DoesNotExist:
            raise self.ProductInvalid()

    @allow_roles(["admin", "manager"])
    def update(self, order_id: int, data: UpdateOrderData, user=None):
        try:
            with self._repo.session() as s:
                for item in data["items"]:
                    product = self._product_repo.get_by_id(
                        item["product_id"], session=s
                    )
                    item["product"] = product

                promo_code_value = data.get("promo_code")
                promo_code = None

                if promo_code_value:
                    promo_code = self._promo_code_repo.get_by_value(
                        promo_code_value.lower(), session=s
                    )

                    if promo_code.disable_on_use:
                        promo_code.is_active = False

                order = self._repo.update_order(
                    order_id,
                    data["user_name"],
                    data["user_phone_number"],
                    data["user_address"],
                    data["items"],
                    data["status"],
                    promo_code,
                    session=s,
                )

                link = app.config.get("HOST") + "/admin/orders/" + str(order.id)
                title = "Заказ обновлен!"
                description = (
                    "Имя: "
                    + order.user_name
                    + "<br/>"
                    + "Телефон: "
                    + order.user_phone_number
                    + "<br/>"
                    + "Адрес: "
                    + order.user_address
                    + "<br/>"
                    + "Статус: "
                    + order.status
                )
                link_text = "Подробнее"
                subject = link_text
                body = render_template(
                    "link_email.html",
                    link=link,
                    title=title,
                    description=description,
                    link_text=link_text,
                    preheader=title,
                )

                self._mail.send(subject, body, [app.config.get("MAIL_ORDERS_USERNAME")])

                return order
        except self._promo_code_repo.DoesNotExist:
            raise self.PromoCodeInvalid()
        except self._product_repo.DoesNotExist:
            raise self.ProductInvalid()
        except self._repo.DoesNotExist:
            raise self.OrderNotFound()

    @allow_roles(["admin", "manager"])
    def get_all(self, offset: int = None, limit: int = None, user: User = None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_for_user(
        self, user_id, offset: int = None, limit: int = None, user: User = None
    ):
        if user and (user.id == user_id or user.group.name in ["admin", "manager"]):
            return self._repo.get_for_user(user_id, offset=offset, limit=limit)
        raise InvalidEntityFormat({"user": "errors.invalid"})

    @allow_roles(["admin", "manager"])
    def get_one(self, id_: int, user: User = None):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.OrderNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.OrderNotFound()

    class ProductInvalid(Exception):
        pass

    class PromoCodeInvalid(Exception):
        pass

    class OrderNotFound(Exception):
        pass
