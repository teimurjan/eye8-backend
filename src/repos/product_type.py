from fileinput import FileInput

from typing import Dict, List

from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy.sql.expression import and_, case, exists, text
from sqlalchemy.sql.functions import func


from src.models import (
    ProductType,
    ProductTypeDescription,
    ProductTypeName,
    ProductTypeShortDescription,
    Category,
    Product,
    ProductTypeInstagramLink,
    FeatureType,
)
from src.repos.base import NonDeletableRepo, set_intl_texts, with_session
from src.storage.base import Storage
from src.utils.slug import generate_slug
from src.utils.sorting import ProductTypeSortingType


def set_instagram_links(product_type, instagram_links):
    instagram_links_ = []
    for link in instagram_links:
        instagram_link = ProductTypeInstagramLink()
        instagram_link.link = link
        instagram_links_.append(instagram_link)
    product_type.instagram_links = instagram_links_


availability_col_expr = case(
    [
        (
            exists()
            .where(
                and_(Product.product_type_id == ProductType.id, Product.quantity > 0)
            )
            .correlate(ProductType),
            1,
        )
    ],
    else_=0,
).label("availability")
min_price_col_expr = func.min(Product.calculated_price).label("min_price")


class ProductTypeRepo(NonDeletableRepo):
    def __init__(self, db_engine, file_storage: Storage):
        super().__init__(db_engine, ProductType)
        self.__file_storage = file_storage

    @with_session
    def add_product_type(
        self,
        names: Dict,
        descriptions: Dict,
        short_descriptions: Dict,
        instagram_links: List[str],
        image: FileInput,
        categories: List[Category],
        feature_types: List[FeatureType],
        session: SQLAlchemySession = None,
    ):
        product_type = ProductType()

        set_intl_texts(names, product_type, "names", ProductTypeName, session=session)
        product_type.slug = self.get_unique_slug(product_type, session=session)
        set_intl_texts(
            descriptions,
            product_type,
            "descriptions",
            ProductTypeDescription,
            session=session,
        )
        set_intl_texts(
            short_descriptions,
            product_type,
            "short_descriptions",
            ProductTypeShortDescription,
            session=session,
        )

        set_instagram_links(product_type, instagram_links)

        for feature_type in feature_types:
            product_type.feature_types.append(feature_type)

        product_type.categories = categories
        product_type.image = self.__file_storage.save_file(image)

        session.add(product_type)
        session.flush()

        product_type.created_on
        product_type.updated_on

        return product_type

    @with_session
    def update_product_type(
        self,
        id_: int,
        names: Dict,
        descriptions: Dict,
        short_descriptions: Dict,
        instagram_links: List[str],
        image: FileInput,
        categories: List[Category],
        feature_types: List[FeatureType],
        session: SQLAlchemySession = None,
    ):
        product_type = self.get_by_id(id_, session=session)

        set_intl_texts(names, product_type, "names", ProductTypeName, session=session)
        set_intl_texts(
            descriptions,
            product_type,
            "descriptions",
            ProductTypeDescription,
            session=session,
        )
        set_intl_texts(
            short_descriptions,
            product_type,
            "short_descriptions",
            ProductTypeShortDescription,
            session=session,
        )

        set_instagram_links(product_type, instagram_links)

        product_type.feature_types = feature_types
        product_type.slug = self.get_unique_slug(product_type, session=session)
        product_type.categories = categories

        if image is not None:
            product_type.image = (
                image
                if isinstance(image, str)
                else self.__file_storage.save_file(image)
            )

        session.flush()

        product_type.created_on
        product_type.updated_on

        return product_type

    @with_session
    def _get_all_query(
        self,
        sorting_type: ProductTypeSortingType = ProductTypeSortingType.DEFAULT,
        session: SQLAlchemySession = None,
    ):
        if sorting_type == ProductTypeSortingType.NEWLY_ADDED:
            return (
                self.get_non_deleted_query(
                    extra_fields=[availability_col_expr], session=session
                )
                .join(Product)
                .group_by(ProductType)
                .order_by(text("availability DESC"), ProductType.id.desc())
            )
        if sorting_type == ProductTypeSortingType.PRICE_ASCENDING:
            return (
                self.get_non_deleted_query(
                    extra_fields=[availability_col_expr, min_price_col_expr],
                    session=session,
                )
                .join(Product)
                .group_by(ProductType)
                .order_by(text("availability DESC, min_price ASC"))
            )
        if sorting_type == ProductTypeSortingType.PRICE_ASCENDING:
            return (
                self.get_non_deleted_query(
                    extra_fields=[availability_col_expr, min_price_col_expr],
                    session=session,
                )
                .join(Product)
                .group_by(ProductType)
                .order_by(text("availability DESC, min_price DESC"))
            )

        return self.get_non_deleted_query().order_by(ProductType.id)

    @with_session
    def get_all(
        self,
        category_ids: List[int] = None,
        sorting_type: ProductTypeSortingType = ProductTypeSortingType.DEFAULT,
        offset: int = None,
        limit: int = None,
        only_available: bool = False,
        session: SQLAlchemySession = None,
    ):

        q = self._get_all_query(sorting_type=sorting_type, session=session)

        q = (
            q.filter(ProductType.categories.any(Category.id.in_(category_ids)))
            if category_ids is not None
            else q
        )

        q = q.filter(Product.is_available == True) if only_available else q

        result = q.offset(offset).limit(limit).all()

        return (
            [item[0] if isinstance(item, tuple) else item for item in result],
            q.count(),
        )

    @with_session
    def has_with_category(self, id_: int, session: SQLAlchemySession = None):
        return (
            self.get_non_deleted_query(session=session)
            .join(ProductType.categories)
            .filter(Category.id.in_([id_]))
            .count()
            > 0
        )

    @with_session
    def is_slug_used(self, slug: str, session: SQLAlchemySession = None):
        return (
            self.get_query(session=session).filter(ProductType.slug == slug).count() > 0
        )

    @with_session
    def get_by_slug(self, slug: str, session: SQLAlchemySession = None):
        return (
            self.get_non_deleted_query(session=session)
            .filter(ProductType.slug == slug)
            .first()
        )

    @with_session
    def get_unique_slug(
        self, product_type: ProductType, session: SQLAlchemySession = None
    ):
        generated_slug = generate_slug(product_type)
        if generated_slug == product_type.slug:
            return generated_slug

        if self.is_slug_used(generated_slug, session=session):
            return generate_slug(product_type, with_hash=True)

        return generated_slug

    class DoesNotExist(Exception):
        pass
