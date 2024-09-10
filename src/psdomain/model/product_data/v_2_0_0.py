from pydantic import Field

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, ProductSellableArray, \
    Product, LocationDecorationArray, ProductPriceGroupArray, FobPointArray


class ProductV200(Product):
    LocationDecorationArray: LocationDecorationArray | None
    ProductPriceGroupArray: ProductPriceGroupArray | None
    FobPointArray: FobPointArray | None


class ProductResponseV200(base.ServiceMessageResponse):
    Product: ProductV200 | None = Field(None, alias='Product', description='Product Information',
                                        title='ProductV200')


class ProductCloseOutResponseV200(base.ServiceMessageResponse):
    ProductCloseOutArray: ProductCloseOutArray | None


class ProductDateModifiedResponseV200(base.ServiceMessageResponse):
    ProductDateModifiedArray: ProductDateModifiedArray | None


class GetProductSellableResponseV200(base.ServiceMessageResponse):
    ProductSellableArray: ProductSellableArray | None
