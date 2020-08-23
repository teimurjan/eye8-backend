from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.repos.base import NonDeletableRepo, with_session
from src.models import User


class UserRepo(NonDeletableRepo):
    def __init__(self, db_engine):
        super().__init__(db_engine, User)

    @with_session
    def get_first_by_email(self, email: str, session: SQLAlchemySession = None):
        return self.get_query(session=session).filter(User.email == email).first()

    @with_session
    def is_email_used(self, email: str, session: SQLAlchemySession = None):
        return (
            self.get_non_deleted_query(session=session)
            .filter(User.email == email)
            .count()
            > 0
        )

    @with_session
    def create_user(
        self, name: str, email: str, password: str, session: SQLAlchemySession
    ):
        user = User()
        user.name = name
        user.email = email
        user.password = password
        user.group_id = 1

        session.add(user)
        session.flush()

        # fetch group within the session for the future use
        user.group

        return user

    class DoesNotExist(Exception):
        pass
