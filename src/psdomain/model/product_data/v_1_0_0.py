from pydantic import Field

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, Product, ProductSellableArray


class ProductV100(Product):
    def get_min_qty(self, currency='USD', configuration_type='Decorated'):
        # because we don't have the information about the price group we will return None
        return None

    @property
    def fob_points(self):
        # there is no fob information in this version
        return []


class ProductResponseV100(base.ErrorMessageResponse):
    Product: ProductV100 | None = Field(None, alias='Product', description='Product Information',
                                        title='Product')


class ProductCloseOutResponseV100(base.ErrorMessageResponse):
    ProductCloseOutArray: ProductCloseOutArray | None


class ProductDateModifiedResponseV100(base.ErrorMessageResponse):
    ProductDateModifiedArray: ProductDateModifiedArray | None


class GetProductSellableResponseV100(base.ErrorMessageResponse):
    ProductSellableArray: ProductSellableArray | None
