from datetime import datetime

from src.repos.currency_rate import CurrencyRateRepo
from src.repos.order import OrderRepo
from src.services.decorators import allow_roles
from src.utils.array import find_in_array


class CurrencyRateService:
    def __init__(self, repo: CurrencyRateRepo, order_repo: OrderRepo):
        self._repo = repo
        self._order_repo = order_repo

    def get_all(self):
        return self._repo.get_all()

    @allow_roles(['admin'])
    def create(self, data, *args, **kwargs):
        if self._repo.exists_for_date(data['name'], datetime.now()):
            raise self.AdditionLimitExceeded()

        return self._repo.add_currency_rate(data['name'], data['value'])

    @allow_roles(['admin'])
    def delete(self, id_, *args, **kwargs):
        rates = self.get_all()

        rate_to_delete_index, rate_to_delete = find_in_array(
            rates, lambda r: r.id == id_)
        if rate_to_delete is None:
            raise self.CurrencyRateNotFound()

        is_last_rate = rate_to_delete_index == len(rates) - 1
        next_rate = None if is_last_rate else rates[rate_to_delete_index + 1]

        if (
            self._order_repo.has_for_date_range(
                rate_to_delete.created_on,
                next_rate.created_on if next_rate else None
            )
        ):
            raise self.CurrencyRateIsUntouchable()
        else:
            self._repo.delete(id_)

    @allow_roles(['admin'])
    def get_one(self, id_, *args, **kwargs):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.CurrencyRateNotFound()

    class CurrencyRateNotFound(Exception):
        pass

    class AdditionLimitExceeded(Exception):
        pass

    class CurrencyRateIsUntouchable(Exception):
        pass
