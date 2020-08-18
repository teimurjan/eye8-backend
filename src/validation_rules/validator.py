from cerberus.validator import Validator

from typing import Dict, Generic, TypeVar, cast

V = TypeVar("V")


class DataValidator(Generic[V]):
    def __init__(self, validation_rules: Dict):
        self._validation_rules = validation_rules

    def validate(self, data: Dict) -> V:
        validator = Validator(self._validation_rules)
        is_valid = validator.validate(data)
        if is_valid:
            return cast(V, data)

        raise self.ValidationError(validator.errors)

    class ValidationError(Exception):
        def __init__(self, errors):
            self.errors = errors
