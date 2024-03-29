from typing import Dict
from sqlalchemy.orm.query import aliased
from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy.sql.functions import func

from src.models import Category
from src.repos.base import Repo, with_session
from src.utils.slug import generate_slug


class CategoryRepo(Repo):
    def __init__(self, db_engine):
        super().__init__(db_engine, Category)

    @with_session
    def add_category(
        self, names: Dict, parent_category_id: int, session: SQLAlchemySession = None,
    ):
        category = Category()

        category.parent_category_id = parent_category_id
        category.name_en = names["en"]
        category.name_ru = names["ru"]
        category.slug = self.get_unique_slug(category, session=session)

        session.add(category)
        session.flush()

        category.created_on
        category.updated_on

        return category

    @with_session
    def update_category(
        self,
        id_: int,
        names: Dict,
        parent_category_id: int,
        session: SQLAlchemySession = None,
    ):
        category = self.get_by_id(id_, session=session)
        category.parent_category_id = parent_category_id
        category.name_en = names["en"]
        category.name_ru = names["ru"]
        category.slug = self.get_unique_slug(category, session=session)

        session.flush()

        category.created_on
        category.updated_on

        return category

    @with_session
    def get_children(self, id_: int, session: SQLAlchemySession = None):
        category_recursive_query = (
            self.get_query(session=session)
            .filter(Category.id == id_)
            .cte(recursive=True)
        )

        category_alias = aliased(category_recursive_query, name="parent")
        children_alias = aliased(Category, name="children")

        final_query = category_recursive_query.union_all(
            session.query(children_alias).filter(
                children_alias.parent_category_id == getattr(category_alias.c, "id")
            )
        )

        return session.query(final_query).all()

    @with_session
    def has_children(self, id_: int, session: SQLAlchemySession = None):
        return (
            self.get_query(session=session)
            .filter(Category.parent_category_id == id_)
            .count()
            > 0
        )

    @with_session
    def is_slug_used(self, slug: str, session: SQLAlchemySession = None):
        return self.get_query(session=session).filter(Category.slug == slug).count() > 0

    @with_session
    def get_by_slug(self, slug: str, session: SQLAlchemySession = None):
        return self.get_query(session=session).filter(Category.slug == slug).first()

    @with_session
    def get_unique_slug(self, category: Category, session: SQLAlchemySession = None):
        generated_slug = generate_slug(category.name_en)
        if generated_slug == category.slug:
            return generated_slug

        if self.is_slug_used(generated_slug, session=session):
            return generate_slug(category.name_en, with_hash=True)

        return generated_slug

    @with_session
    def search(self, query: str, session: SQLAlchemySession = None):
        return (
            self.get_query(session=session)
            .filter(func.lower(Category.name_en).like(f"%{query.lower()}%"))
            .limit(7)
        )

    class DoesNotExist(Exception):
        pass
