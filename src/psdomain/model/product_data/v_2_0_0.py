from pydantic import Field

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, ProductSellableArray, \
    Product, LocationDecorationArray, ProductPriceGroupArray, FobPointArray


class ProductV200(Product):
    LocationDecorationArray: LocationDecorationArray | None
    ProductPriceGroupArray: ProductPriceGroupArray | None
    FobPointArray: FobPointArray | None


class ProductResponseV200(base.PSBaseModel):
    Product: ProductV200 | None = Field(None, alias='Product', description='Product Information',
                                        title='ProductV200')
    ServiceMessageArray: base.ServiceMessageArray | None = None

    @property
    def is_ok(self):
        return self.ServiceMessageArray is None


class ProductCloseOutResponseV200(base.PSBaseModel):
    ProductCloseOutArray: ProductCloseOutArray | None
    ServiceMessageArray: base.ServiceMessageArray | None


class ProductDateModifiedResponseV200(base.PSBaseModel):
    ProductDateModifiedArray: ProductDateModifiedArray | None
    ServiceMessageArray: base.ServiceMessageArray | None


class GetProductSellableResponseV200(base.PSBaseModel):
    ProductSellableArray: ProductSellableArray | None
    ServiceMessageArray: base.ServiceMessageArray | None = None

    @property
    def is_ok(self):
        return self.ServiceMessageArray is None or not self.ServiceMessageArray.ServiceMessage
