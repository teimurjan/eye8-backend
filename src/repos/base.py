from contextlib import contextmanager
from typing import Any, Dict, Iterator, Type, TypeVar, List

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy.orm.query import Query as SQLAlchemyQuery

T = TypeVar("T")


def with_session(f):
    def wrapper(self, *args, **kwargs):
        if kwargs.get("session") is None:
            with self.session() as s:
                kwargs["session"] = s
                return f(self, *args, **kwargs)
        return f(self, *args, **kwargs)

    return wrapper


class Repo:
    def __init__(self, db_engine, model_cls: Type[T]):
        self.__db_engine = db_engine
        self._model_cls = model_cls

    @contextmanager
    def session(self) -> Iterator[SQLAlchemySession]:
        Session = sessionmaker(bind=self.__db_engine)
        session = Session()
        session.expire_on_commit = False
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    @with_session
    def get_query(
        self, extra_fields: List[Any] = [], session: SQLAlchemySession = None
    ) -> SQLAlchemyQuery:
        return session.query(self._model_cls, *extra_fields)

    @with_session
    def get_by_id(self, id_: int, session: SQLAlchemySession = None) -> T:
        obj = self.get_query(session=session).get(id_)
        if obj is None:
            raise self.DoesNotExist()

        return obj

    @with_session
    def get_all(
        self, offset: int = None, limit: int = None, session: SQLAlchemySession = None
    ) -> List[T]:
        return (
            self.get_query(session=session)
            .order_by(self._model_cls.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @with_session
    def count_all(self, session: SQLAlchemySession = None) -> int:
        return self.get_query(session=session).count()

    @with_session
    def filter_by_ids(
        self, ids: List[int], limit: int = None, session: SQLAlchemySession = None
    ) -> List[T]:
        return (
            self.get_query(session=session)
            .filter(self._model_cls.id.in_(ids))
            .limit(limit)
            .all()
        )

    @with_session
    def delete(self, id_: int, session: SQLAlchemySession = None) -> None:
        obj = self.get_by_id(id_, session=session)
        return session.delete(obj)

    class DoesNotExist(Exception):
        def __new__(cls, *args, **kwargs):
            raise NotImplementedError


class NonDeletableRepo(Repo):
    def __init__(self, db_engine, model_cls: Type[T]):
        super().__init__(db_engine, model_cls)

    @with_session
    def delete(self, id_: int, session: SQLAlchemySession = None):
        obj = self.get_by_id(id_, session=session)
        obj.is_deleted = True
        return obj

    @with_session
    def delete_forever(self, id_: int, session: SQLAlchemySession = None):
        obj = self.get_by_id(id_, deleted=True, session=session)
        session.delete(obj)

    @with_session
    def get_deleted_query(
        self, extra_fields: List[Any] = [], session: SQLAlchemySession = None
    ):
        return self.get_query(extra_fields=extra_fields, session=session).filter(
            self._model_cls.is_deleted == True
        )

    @with_session
    def get_non_deleted_query(
        self, extra_fields: List[Any] = [], session: SQLAlchemySession = None
    ) -> SQLAlchemyQuery:
        return self.get_query(extra_fields=extra_fields, session=session).filter(
            (self._model_cls.is_deleted == None) | (self._model_cls.is_deleted == False)
        )

    @with_session
    def get_by_id(self, id_: int, deleted=False, session: SQLAlchemySession = None):
        q = (
            self.get_deleted_query(session=session)
            if deleted
            else self.get_non_deleted_query(session=session)
        )

        obj = q.filter(self._model_cls.id == id_).first()
        if obj is None:
            raise self.DoesNotExist()

        return obj

    @with_session
    def get_all(
        self, offset=None, limit=None, deleted=False, session: SQLAlchemySession = None,
    ):
        q = (
            self.get_deleted_query(session=session)
            if deleted
            else self.get_non_deleted_query(session=session)
        )

        return q.order_by(self._model_cls.id).offset(offset).limit(limit).all()

    @with_session
    def count_all(self, session: SQLAlchemySession = None):
        return self.get_non_deleted_query(session=session).count()

    @with_session
    def filter_by_ids(
        self, ids: List[int], limit: int = None, session: SQLAlchemySession = None
    ):
        return (
            self.get_non_deleted_query(session=session)
            .filter(self._model_cls.id.in_(ids))
            .limit(limit)
            .all()
        )

