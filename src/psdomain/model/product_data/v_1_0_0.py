from pydantic import Field

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, Product, ProductSellableArray


class ProductV100(Product):
    pass


class ProductResponseV100(base.ErrorMessageResponse):
    Product: ProductV100 | None = Field(None, alias='Product', description='Product Information',
                                        title='Product')


class ProductCloseOutResponseV100(base.ErrorMessageResponse):
    ProductCloseOutArray: ProductCloseOutArray | None


class ProductDateModifiedResponseV100(base.ErrorMessageResponse):
    ProductDateModifiedArray: ProductDateModifiedArray | None


class GetProductSellableResponseV100(base.ErrorMessageResponse):
    ProductSellableArray: ProductSellableArray | None
