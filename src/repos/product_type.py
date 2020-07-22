from typing import List

from sqlalchemy import asc, desc, func, orm

from src.models import (ProductType, ProductTypeDescription, ProductTypeName,
                        ProductTypeShortDescription, Category)
from src.models.product import Product
from src.models.product_type.instagram_link import ProductTypeInstagramLink
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


class ProductTypeRepo(NonDeletableRepo):
    def __init__(self, db_conn, file_storage: Storage):
        super().__init__(db_conn, ProductType)
        self.__file_storage = file_storage

    @with_session
    def add_product_type(
        self,
        names,
        descriptions,
        short_descriptions,
        instagram_links,
        image,
        categories,
        feature_types,
        session
    ):
        product_type = ProductType()

        set_intl_texts(names, product_type, 'names',
                       ProductTypeName, session=session)
        product_type.slug = self.get_unique_slug(product_type, session=session)
        set_intl_texts(descriptions, product_type,
                       'descriptions', ProductTypeDescription, session=session)
        set_intl_texts(short_descriptions, product_type,
                       'short_descriptions', ProductTypeShortDescription, session=session)

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
        id_,
        names,
        descriptions,
        short_descriptions,
        instagram_links,
        image,
        categories,
        feature_types,
        session
    ):
        product_type = self.get_by_id(id_, session=session)

        set_intl_texts(names, product_type, 'names',
                       ProductTypeName, session=session)
        set_intl_texts(
            descriptions, product_type, 'descriptions', ProductTypeDescription, session=session)
        set_intl_texts(short_descriptions, product_type,
                       'short_descriptions', ProductTypeShortDescription, session=session)

        set_instagram_links(product_type, instagram_links)

        product_type.feature_types = feature_types
        product_type.slug = self.get_unique_slug(product_type, session=session)
        product_type.categories = categories

        if image is not None:
            product_type.image = (image
                                  if isinstance(image, str)
                                  else self.__file_storage.save_file(image))

        session.flush()

        product_type.created_on
        product_type.updated_on

        return product_type

    @with_session
    def get_all(
        self,
        category_ids: List[int] = None,
        sorting_type: ProductTypeSortingType = ProductTypeSortingType.DEFAULT,
        offset: int = None,
        limit: int = None,
        join_products: bool = False,
        only_available: bool = False,
        session=None,
    ):
        q = self.get_non_deleted_query(session=session)

        if category_ids is not None:
            q = q.join(ProductType.categories).filter(
                Category.id.in_(category_ids))

        if join_products:
            q = (
                q
                .options(orm.joinedload(ProductType.products))
                .outerjoin(ProductType.products)
                .group_by(ProductType.id)
                .group_by(Product.price)
                .group_by(Product.discount)
            )

            if only_available:
                q = q.filter(ProductType.is_available == True)

        q = q.order_by(self._get_order_by_from_sorting_type(sorting_type))

        return q.offset(offset).limit(limit).all(), q.count()

    def _get_order_by_from_sorting_type(self, sorting_type: ProductTypeSortingType):
        if sorting_type == ProductTypeSortingType.PRICE_ASCENDING:
            return asc(Product.calculated_price)
        if sorting_type == ProductTypeSortingType.PRICE_DESCENDING:
            return desc(Product.calculated_price)
        if sorting_type == ProductTypeSortingType.NEWLY_ADDED:
            return ProductType.id.desc()

        return ProductType.id

    @with_session
    def has_with_category(self, id_, session):
        return self.get_non_deleted_query(session=session).join(ProductType.categories).filter(Category.id.in_([id_])).count() > 0

    @with_session
    def is_slug_used(self, slug, session):
        return self.get_query(session=session).filter(ProductType.slug == slug).count() > 0

    @with_session
    def get_by_slug(self, slug, session):
        return self.get_non_deleted_query(session=session).filter(ProductType.slug == slug).first()

    @with_session
    def get_unique_slug(self, product_type, session):
        generated_slug = generate_slug(product_type)
        if generated_slug == product_type.slug:
            return generated_slug

        if self.is_slug_used(generated_slug, session=session):
            return generate_slug(product_type, with_hash=True)

        return generated_slug

    class DoesNotExist(Exception):
        pass
