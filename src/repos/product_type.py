from fileinput import FileInput

from typing import Dict, List

from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy import select, func

from src.models import (
    ProductType,
    Category,
    ProductTypeInstagramLink,
    FeatureType,
    Product,
    CharacteristicValue,
)
from src.repos.base import NonDeletableRepo, with_session
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
        characteristic_values: List[CharacteristicValue],
        session: SQLAlchemySession = None,
    ):
        product_type = ProductType()

        product_type.name_en = names['en']
        product_type.name_ru = names['ru']
        product_type.description_en = descriptions['en']
        product_type.description_ru = descriptions['ru']
        product_type.short_description_en = short_descriptions['en']
        product_type.short_description_ru = short_descriptions['ru']
        product_type.slug = self.get_unique_slug(product_type, session=session)
        set_instagram_links(product_type, instagram_links)
        product_type.feature_types = feature_types
        product_type.characteristic_values = characteristic_values
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
        characteristic_values: List[CharacteristicValue],
        session: SQLAlchemySession = None,
    ):
        product_type = self.get_by_id(id_, session=session)

        product_type.name_en = names['en']
        product_type.name_ru = names['ru']
        product_type.description_en = descriptions['en']
        product_type.description_ru = descriptions['ru']
        product_type.short_description_en = short_descriptions['en']
        product_type.short_description_ru = short_descriptions['ru']
        set_instagram_links(product_type, instagram_links)
        product_type.feature_types = feature_types
        product_type.characteristic_values = characteristic_values
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
    def get_all(
        self,
        category_ids: List[int] = None,
        sorting_type: ProductTypeSortingType = ProductTypeSortingType.DEFAULT,
        characteristic_values_ids: List[int] = None,
        offset: int = None,
        limit: int = None,
        available=False,
        deleted=False,
        session: SQLAlchemySession = None,
    ):
        q_params = {
            "order_by": [ProductType.id],
        }

        if sorting_type == ProductTypeSortingType.NEWLY_ADDED:
            q_params["order_by"] = [
                ProductType.products_available.desc(),
                ProductType.id.desc(),
            ]
        if sorting_type == ProductTypeSortingType.PRICE_ASCENDING:
            q_params["order_by"] = [
                ProductType.products_available.desc(),
                ProductType.products_min_price.asc(),
            ]
        if sorting_type == ProductTypeSortingType.PRICE_DESCENDING:
            q_params["order_by"] = [
                ProductType.products_available.desc(),
                ProductType.products_min_price.desc(),
            ]

        categories_filter = (
            ProductType.categories.any(Category.id.in_(category_ids))
            if category_ids is not None
            else True
        )

        characteristic_values_filter = (
            ProductType.characteristic_values.any(
                CharacteristicValue.id.in_(characteristic_values_ids)
            )
            if characteristic_values_ids is not None
            else True
        )

        q = (
            self.get_deleted_query(session=session)
            if deleted
            else self.get_non_deleted_query(session=session)
        )
        q = (
            q.filter(categories_filter)
            .filter(self.__get_availability_filter() if available else True)
            .filter(characteristic_values_filter)
            .order_by(*q_params["order_by"])
        )

        return q.offset(offset).limit(limit).all(), q.count()

    @with_session
    def search(
        self,
        query: str,
        available=False,
        deleted=False,
        offset: int = None,
        limit: int = None,
        session: SQLAlchemySession = None,
    ):
        search_treshold = 0.1
        query = select([ProductType.id]).where(
            func.similarity(ProductType.name_en, query) > search_treshold
        )
        ids = [row[0] for row in session.connection().execute(query)]

        q = (
            (
                self.get_deleted_query(session=session)
                if deleted
                else self.get_non_deleted_query(session=session)
            )
            .filter(ProductType.id.in_(ids))
            .filter(self.__get_availability_filter() if available else True)
        )

        return q.offset(offset).limit(limit).all(), q.count()

    def __get_availability_filter(self):
        return ProductType.products.any(Product.quantity > 0)

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
        generated_slug = generate_slug(product_type.name_en)
        if generated_slug == product_type.slug:
            return generated_slug

        if self.is_slug_used(generated_slug, session=session):
            return generate_slug(product_type.name_en, with_hash=True)

        return generated_slug

    @with_session
    def delete(self, id_: int, session: SQLAlchemySession = None):
        product_type = self.get_by_id(id_, session=session)
        product_type.is_deleted = True

        for product in product_type.products:
            product.is_deleted = True

        return product_type

    class DoesNotExist(Exception):
        pass
