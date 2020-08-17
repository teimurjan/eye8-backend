from typing import Optional

from flask import Request as FlaskRequest

from src.models import Language, User


class Request(FlaskRequest):
    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, language: Language):
        self.__language = language

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: Optional[User]):
        self.__user = user
