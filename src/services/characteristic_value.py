from src.validation_rules.characteristic_value.update import (
    UpdateCharacteristicValueData,
)
from src.validation_rules.characteristic_value.create import (
    CreateCharacteristicValueData,
)
from src.services.decorators import allow_roles
from src.repos.characteristic_value import CharacteristicValueRepo
from src.repos.characteristic import CharacteristicRepo


class CharacteristicValueService:
    def __init__(
        self, repo: CharacteristicValueRepo, characteristic_repo: CharacteristicRepo
    ):
        self._repo = repo
        self._characteristic_repo = characteristic_repo

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateCharacteristicValueData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                characteristic = self._characteristic_repo.get_by_id(
                    data["characteristic_id"], session=s
                )

                characteristic_value = self._repo.add_characteristic_value(
                    data["names"], characteristic, session=s
                )

                return characteristic_value
        except self._characteristic_repo.DoesNotExist:
            raise self.CharacteristicInvalid()

    @allow_roles(["admin", "manager"])
    def update(self, id_: int, data: UpdateCharacteristicValueData, *args, **kwargs):
        try:
            with self._repo.session() as s:
                characteristic = self._characteristic_repo.get_by_id(
                    data["characteristic_id"], session=s
                )

                return self._repo.update_characteristic_value(
                    id_, data["names"], characteristic=characteristic, session=s
                )
        except self._characteristic_repo.DoesNotExist:
            raise self.CharacteristicInvalid()

    def get_all(self, offset: int = None, limit: int = None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_one(self, id_):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.CharacteristicValueNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.CharacteristicValueNotFound()

    class CharacteristicValueNotFound(Exception):
        pass

    class CharacteristicInvalid(Exception):
        pass
