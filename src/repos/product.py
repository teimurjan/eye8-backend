from fileinput import FileInput
from typing import List, Union, cast
from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.storage.base import Storage
from src.models import ProductImage, Product, ProductType, FeatureValue
from src.repos.base import NonDeletableRepo, with_session


class ProductRepo(NonDeletableRepo):
    def __init__(self, db_engine, file_storage: Storage):
        super().__init__(db_engine, Product)
        self.__file_storage = file_storage

    @with_session
    def add_product(
        self,
        price: int,
        discount: int,
        quantity: int,
        images: List[FileInput],
        product_type: ProductType,
        feature_values: List[FeatureValue],
        session: SQLAlchemySession = None,
    ):
        product = Product()

        product.price = price
        product.discount = discount
        product.quantity = quantity
        product.feature_values = feature_values
        product.product_type = product_type

        for image in images:
            product_image = ProductImage()
            product_image.image = self.__file_storage.save_file(image)
            product.images.append(product_image)

        session.add(product)
        session.flush()

        product.images
        product.created_on
        product.updated_on

        return product

    @with_session
    def update_product(
        self,
        id_: int,
        price: int,
        discount: int,
        quantity: int,
        images: List[Union[FileInput, str]],
        product_type: ProductType,
        feature_values: List[FeatureValue],
        session: SQLAlchemySession = None,
    ):
        product = self.get_by_id(id_, session=session)

        product.price = price
        product.discount = discount
        product.quantity = quantity
        product.feature_values = feature_values
        product.product_type = product_type

        new_images = []
        for image in images:
            if type(image) == str:
                new_images.append(
                    [
                        product_image
                        for product_image in product.images
                        if product_image.image == image
                    ][0]
                )
            else:
                product_image = ProductImage()
                product_image.image = self.__file_storage.save_file(
                    cast(FileInput, image)
                )
                new_images.append(product_image)
        product.images = new_images

        session.flush()

        product.created_on
        product.updated_on

        return product

    @with_session
    def has_with_product_type(
        self, product_type_id: int, session: SQLAlchemySession = None
    ):
        return (
            self.get_query(session=session)
            .filter(Product.product_type_id == product_type_id)
            .count()
            > 0
        )

    @with_session
    def get_all(
        self,
        product_type_id: int = None,
        available=False,
        offset=None,
        limit=None,
        deleted=False,
        session: SQLAlchemySession = None,
    ):
        q = (
            self.get_deleted_query(session=session)
            if deleted
            else self.get_non_deleted_query(session=session)
        )

        q = (
            q.filter(Product.available == True if available else True)
            .filter(
                Product.product_type_id == product_type_id
                if product_type_id is not None
                else True
            )
            .order_by(
                Product.quantity.desc(),
                Product.id if product_type_id is not None else self._model_cls.id,
            )
        )

        return q.offset(offset).limit(limit).all(), q.count()

    class DoesNotExist(Exception):
        pass
