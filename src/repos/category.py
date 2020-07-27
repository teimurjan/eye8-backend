from sqlalchemy.orm.query import aliased

from src.models import Category, CategoryName, FeatureType
from src.repos.base import Repo, set_intl_texts, with_session
from src.utils.slug import generate_slug


class CategoryRepo(Repo):
    def __init__(self, db_conn):
        super().__init__(db_conn, Category)

    @with_session
    def add_category(self, names, parent_category_id, session):
        category = Category()
        category.parent_category_id = parent_category_id

        set_intl_texts(names, category, 'names', CategoryName, session=session)
        category.slug = self.get_unique_slug(category, session=session)

        session.add(category)
        session.flush()

        category.created_on
        category.updated_on


        return category

    @with_session
    def update_category(self, id_, names, parent_category_id, session):
        category = self.get_by_id(id_, session=session)
        category.parent_category_id = parent_category_id

        set_intl_texts(names, category, 'names', CategoryName, session=session)
        category.slug = self.get_unique_slug(category, session=session)

        session.flush()

        category.created_on
        category.updated_on

        return category

    @with_session
    def get_children(self, id_, session):
        category_recursive_query = (
            self
            .get_query(session=session)
            .filter(Category.id == id_)
            .cte(recursive=True)
        )

        category_alias = aliased(category_recursive_query, name="parent")
        children_alias = aliased(Category, name='children')

        final_query = category_recursive_query.union_all(
            session.query(children_alias)
            .filter(
                children_alias.parent_category_id == category_alias.c.id
            )
        )

        return session.query(final_query).all()

    @with_session
    def has_children(self, id_, session):
        return self.get_query(session=session).filter(Category.parent_category_id == id_).count() > 0

    @with_session
    def is_slug_used(self, slug, session):
        return self.get_query(session=session).filter(Category.slug == slug).count() > 0

    @with_session
    def get_by_slug(self, slug, session):
        return self.get_query(session=session).filter(Category.slug == slug).first()

    @with_session
    def get_unique_slug(self, category, session):
        generated_slug = generate_slug(category)
        if generated_slug == category.slug:
            return generated_slug

        if self.is_slug_used(generated_slug, session=session):
            return generate_slug(category, with_hash=True)

        return generated_slug

    class DoesNotExist(Exception):
        pass