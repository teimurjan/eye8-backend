from typing import List, Optional, TypedDict
from enum import Enum

from flask import Request as FlaskRequest

from src.models import Language, User


class SideEffectType(Enum):
    SetCookie = "set_cookie"


class SideEffect:
    def __init__(self, type: SideEffectType, data: dict):
        self.type = type
        self.data = data


class Request(FlaskRequest):
    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        setattr(self, "__language", None)
        setattr(self, "__user", None)
        setattr(self, "__side_effects", [])

    @property
    def language(self):
        return getattr(self, "__language")

    @language.setter
    def language(self, language: Language):
        setattr(self, "__language", language)

    @property
    def user(self):
        return getattr(self, "__user")

    @user.setter
    def user(self, user: Optional[User]):
        setattr(self, "__user", user)

    @property
    def side_effects(self):
        return getattr(self, "__side_effects")

    @side_effects.setter
    def side_effects(self, side_effects: List[SideEffect]):
        setattr(self, "__side_effects", side_effects)
