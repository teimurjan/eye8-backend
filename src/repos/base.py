from contextlib import contextmanager
from typing import Generic, TypeVar, List

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from src.models.intl import Language

T = TypeVar('T')


def with_session(f):
    def wrapper(self, *args, **kwargs):
        if kwargs.get('session') is None:
            with self.session() as s:
                kwargs['session'] = s
                return f(self, *args, **kwargs)
        return f(self, *args, **kwargs)

    return wrapper


class Repo(Generic[T]):
    def __init__(self, db_conn, Model: T):
        self.__db_conn = db_conn
        self._Model = Model

    @contextmanager
    def session(self):
        Session = sessionmaker(bind=self.__db_conn, expire_on_commit=False)
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @with_session
    def get_query(self, session=None):
        return session.query(self._Model)

    @with_session
    def get_by_id(self, id_, session) -> T:
        obj = self.get_query(session=session).get(id_)
        if obj is None:
            raise self.DoesNotExist()

        return obj

    @with_session
    def get_all(self, offset=None, limit=None, session=None) -> List[T]:
        return self.get_query(session=session).order_by(self._Model.id).offset(offset).limit(limit).all()

    @with_session
    def count_all(self, session=None) -> int:
        return self.get_query(session=session).count()

    @with_session
    def filter_by_ids(self, ids, session) -> List[T]:
        return self.get_query(session=session).filter(self._Model.id.in_(ids)).all()

    @with_session
    def delete(self, id_, session) -> None:
        obj = self.get_by_id(id_, session=session)
        return session.delete(obj)

    class DoesNotExist(Exception):
        def __new__(cls, *args, **kwargs):
            raise NotImplementedError


class NonDeletableRepo(Repo[T]):
    def __init__(self, db_conn, Model: T):
        super().__init__(db_conn, Model)

    @with_session
    def delete(self, id_, session):
        obj = self.get_by_id(id_, session=session)
        obj.is_deleted = True
        return obj

    @with_session
    def get_deleted_query(self, session=None):
        return self.get_query(session=session).filter(self._Model.is_deleted == True)

    @with_session
    def get_non_deleted_query(self, session=None):
        return self.get_query(session=session).filter((self._Model.is_deleted == None) | (self._Model.is_deleted == False))

    @with_session
    def get_by_id(self, id_, session=None):
        obj = (
            self
            .get_non_deleted_query(session=session)
            .filter(self._Model.id == id_)
            .first()
        )
        if obj is None:
            raise self.DoesNotExist()

        return obj

    @with_session
    def get_all(self, offset=None, limit=None, session=None):
        return self.get_non_deleted_query(session=session).order_by(self._Model.id).offset(offset).limit(limit).all()

    @with_session
    def count_all(self, session=None):
        return self.get_non_deleted_query(session=session).count()

    @with_session
    def filter_by_ids(self, ids, session=None):
        return self.get_non_deleted_query(session=session).filter(self._Model.id.in_(ids)).all()


def set_intl_texts(texts, owner, owner_field_name, IntlTextModel, session):
    new_texts = []
    for language_id, value in texts.items():
        text = IntlTextModel()
        text.value = value
        language = session.query(Language).get(int(language_id))
        text.language = language
        new_texts.append(text)

    setattr(owner, owner_field_name, new_texts)
