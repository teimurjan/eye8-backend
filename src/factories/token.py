import datetime
from time import mktime
from src.models.user import User
import jwt
from flask import current_app as app

ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
SIGNUP_TOKEN_TYPE = "signup"


class TokenFactory:
    @staticmethod
    def create(type_, entity: User):
        if type_ == ACCESS_TOKEN_TYPE:
            exp_date = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
            exp_date_seconds = mktime(exp_date.timetuple())
            payload = {
                "user_id": entity.id,
                "name": entity.name,
                "group": entity.group.name,
                "exp": exp_date_seconds,
            }
            return jwt.encode(payload, app.config["SECRET_KEY"]).decode()
        elif type_ == REFRESH_TOKEN_TYPE:
            exp_date = datetime.datetime.utcnow() + datetime.timedelta(days=10)
            exp_date_seconds = mktime(exp_date.timetuple())
            payload = {"user_id": entity.id, "exp": exp_date_seconds}
            return jwt.encode(payload, app.config["SECRET_KEY"]).decode()
        elif type_ == SIGNUP_TOKEN_TYPE:
            exp_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            exp_date_seconds = mktime(exp_date.timetuple())
            payload = {
                "user_name": entity.user_name,
                "user_email": entity.user_email,
                "exp": exp_date_seconds,
            }
            return jwt.encode(payload, app.config["SECRET_KEY"]).decode()
        else:
            raise Exception("Unknown token type")
