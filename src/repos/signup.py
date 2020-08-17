import bcrypt

from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import Repo, with_session
from src.models import Signup


def encrypt_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


class SignupRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, Signup)

    @with_session
    def get_first_by_email(self, email: str, session: SQLAlchemySession):
        return (
            self.get_query(session=session).filter(Signup.user_email == email).first()
        )

    @with_session
    def is_email_used(self, email: str, session: SQLAlchemySession):
        return (
            self.get_query(session=session).filter(Signup.emuser_ail == email).count()
            > 0
        )

    @with_session
    def create_signup(
        self, name: str, email: str, password: str, session: SQLAlchemySession
    ):
        signup = Signup()
        signup.user_name = name
        signup.user_email = email
        signup.user_password = encrypt_password(password)

        session.add(signup)
        session.flush()

        return signup

    @with_session
    def update_signup(
        self, signup_id: int, name: str, password: str, session: SQLAlchemySession
    ):
        signup = self.get_by_id(signup_id, session=session)
        signup.user_name = name
        signup.user_password = encrypt_password(password)

        return signup

    class DoesNotExist(Exception):
        pass
