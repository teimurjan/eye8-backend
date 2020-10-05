from src.validation_rules.characteristic.create import CreateCharacteristicData
from src.validation_rules.characteristic.update import UpdateCharacteristicData
from src.services.decorators import allow_roles
from src.repos.characteristic import CharacteristicRepo


class CharacteristicService:
    def __init__(self, repo: CharacteristicRepo):
        self._repo = repo

    @allow_roles(["admin", "manager"])
    def create(self, data: CreateCharacteristicData, *args, **kwargs):
        characteristic = self._repo.add_characteristic(data["names"])
        return characteristic

    @allow_roles(["admin", "manager"])
    def update(
        self, characteristic_id: int, data: UpdateCharacteristicData, *args, **kwargs
    ):
        return self._repo.update_characteristic(characteristic_id, data["names"])

    def get_all(self, offset: int = None, limit: int = None):
        return self._repo.get_all(offset=offset, limit=limit), self._repo.count_all()

    def get_one(self, id_: int):
        try:
            return self._repo.get_by_id(id_)
        except self._repo.DoesNotExist:
            raise self.CharacteristicNotFound()

    @allow_roles(["admin", "manager"])
    def delete(self, id_: int, *args, **kwargs):
        try:
            return self._repo.delete(id_)
        except self._repo.DoesNotExist:
            raise self.CharacteristicNotFound()

    class CharacteristicNotFound(Exception):
        pass
