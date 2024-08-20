# will not only represent the latest version of the product data, but also be flexible enough to represent any
# version of the product data.
import typing

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, Product, LocationDecorationArray, \
    ProductPriceGroupArray, FobPointArray


class ProductLatest(Product):
    LocationDecorationArray: typing.Optional[LocationDecorationArray] = None  # in V1 is not required
    ProductPriceGroupArray: typing.Optional[ProductPriceGroupArray] = None  # in V1 is not required
    FobPointArray: typing.Optional[FobPointArray] = None  # in V1 is not required


class ProductResponseLatest(base.PSBaseModel):
    Product: ProductLatest | None
    ServiceMessageArray: base.ServiceMessageArray | None = None
    ErrorMessage: base.ErrorMessage | None = None

    @property
    def is_ok(self):
        return self.ServiceMessageArray is None and self.ErrorMessage is None


class ProductCloseOutResponseLatest(base.PSBaseModel):
    ProductCloseOutArray: ProductCloseOutArray | None
    ServiceMessageArray: base.ServiceMessageArray | None = None
    ErrorMessage: base.ErrorMessage | None = None


class ProductDateModifiedResponseLatest(base.PSBaseModel):
    ProductDateModifiedArray: ProductDateModifiedArray | None
    ServiceMessageArray: base.ServiceMessageArray | None = None
    ErrorMessage: base.ErrorMessage | None = None
