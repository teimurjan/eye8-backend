from fileinput import FileInput
from typing import List, Optional, Union, cast
from sqlalchemy.orm.session import Session as SQLAlchemySession

from src.storage.base import Storage
from src.models import ProductImage, Product, ProductType, FeatureValue
from src.repos.base import NonDeletableRepo, with_session


class ProductRepo(NonDeletableRepo):
    def __init__(self, db_conn, file_storage: Storage):
        super().__init__(db_conn, Product)
        self.__file_storage = file_storage

    @with_session
    def add_product(
        self,
        price: int,
        discount: int,
        quantity: int,
        upc: Optional[str],
        images: List[FileInput],
        product_type: ProductType,
        feature_values: List[FeatureValue],
        session: SQLAlchemySession,
    ):
        product = Product()

        product.price = price
        product.discount = discount
        product.quantity = quantity
        product.upc = upc
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
        upc: Optional[str],
        images: List[Union[FileInput, str]],
        product_type: ProductType,
        feature_values: List[FeatureValue],
        session: SQLAlchemySession,
    ):
        product = self.get_by_id(id_, session=session)

        product.price = price
        product.discount = discount
        product.quantity = quantity
        product.upc = upc
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
    def has_with_product_type(self, product_type_id: int, session: SQLAlchemySession):
        return (
            self.get_non_deleted_query(session=session)
            .filter(Product.product_type_id == product_type_id)
            .count()
            > 0
        )

    @with_session
    def get_first_by_upc(self, upc: str, session: SQLAlchemySession):
        return self.get_query(session=session).filter(Product.upc == upc).first()

    @with_session
    def get_for_product_type(
        self, product_type_id: int, session: SQLAlchemySession = None
    ):
        return (
            self.get_query(session=session)
            .filter(Product.product_type_id == product_type_id)
            .order_by(Product.quantity.desc(), Product.id)
            .all()
        )

    class DoesNotExist(Exception):
        pass
