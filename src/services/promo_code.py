from src.repos.order import OrderRepo
from src.repos.product import ProductRepo
from src.repos.promo_code import PromoCodeRepo
from src.services.decorators import allow_roles


class PromoCodeService:
    def __init__(
        self, repo: PromoCodeRepo, product_repo: ProductRepo, order_repo: OrderRepo
    ):
        self._repo = repo
        self._product_repo = product_repo
        self._order_repo = order_repo

    @allow_roles(["admin", "manager"])
    def create(self, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                products = self._product_repo.filter_by_ids(data["products"], session=s)
                return self._repo.add_promo_code(
                    data["value"].lower(),
                    data["discount"],
                    data.get("amount"),
                    data.get("is_active", False),
                    data.get("disable_on_use", False),
                    products,
                    session=s,
                )
        except self._repo.ValueNotUnique:
            raise self.ValueNotUnique()

    @allow_roles(["admin", "manager"])
    def update(self, id_, data, *args, **kwargs):
        try:
            with self._repo.session() as s:
                if self._order_repo.has_with_promo_code(id_, session=s):
                    raise self.PromoCodeWithOrdersIsUntouchable()

                products = self._product_repo.filter_by_ids(data["products"], session=s)
                return self._repo.update_promo_code(
                    id_, data["is_active"], data["disable_on_use"], products, session=s
                )
        except self._repo.ValueNotUnique:
            raise self.ValueNotUnique()

    @allow_roles(["admin", "manager"])
    def get_all(self, offset=None, limit=None, deleted=False, *args, **kwargs):
        return (
            self._repo.get_all(offset=offset, limit=limit, deleted=deleted),
            self._repo.count_all(),
        )

    def get_one(self, id_, deleted=False):
        try:
            promo_code = self._repo.get_by_id(id_, deleted=deleted)
            return promo_code
        except self._repo.DoesNotExist:
            raise self.PromoCodeNotFound()

    def get_one_by_value(self, value):
        try:
            promo_code = self._repo.get_by_value(value)
            if not promo_code.is_active:
                raise self.PromoCodeNotFound()
            return promo_code
        except self._repo.DoesNotExist:
            raise self.PromoCodeNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_, *args, **kwargs):
        try:
            with self._repo.session() as s:
                if self._order_repo.has_with_promo_code(id_, session=s):
                    raise self.PromoCodeWithOrdersIsUntouchable()

                return self._repo.delete(id_, session=s)
        except self._repo.DoesNotExist:
            raise self.PromoCodeNotFound()

    @allow_roles(["admin", "manager"])
    def delete_instantly(self, id_, *args, **kwargs):
        try:
            with self._repo.session() as s:
                if self._order_repo.has_with_promo_code(id_, session=s):
                    raise self.PromoCodeWithOrdersIsUntouchable()

                return self._repo.delete_instantly(id_, session=s)
        except self._repo.DoesNotExist:
            raise self.PromoCodeNotFound()

    class PromoCodeNotFound(Exception):
        pass

    class ValueNotUnique(Exception):
        pass

    class PromoCodeWithOrdersIsUntouchable(Exception):
        pass
