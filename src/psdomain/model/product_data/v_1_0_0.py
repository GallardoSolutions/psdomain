from pydantic import Field

from .. import base
from .common import ProductCloseOutArray, ProductDateModifiedArray, Product, ProductSellableArray


class ProductV100(Product):
    pass


class ProductResponseV100(base.PSBaseModel):
    Product: ProductV100 | None = Field(None, alias='Product', description='Product Information',
                                        title='Product')
    ErrorMessage: base.ErrorMessage | None = None

    @property
    def is_ok(self):
        return self.ErrorMessage is None


class ProductCloseOutResponseV100(base.PSBaseModel):
    ProductCloseOutArray: ProductCloseOutArray | None
    ErrorMessage: base.ErrorMessage | None


class ProductDateModifiedResponseV100(base.PSBaseModel):
    ProductDateModifiedArray: ProductDateModifiedArray | None
    ErrorMessage: base.ErrorMessage | None = None


class GetProductSellableResponseV100(base.PSBaseModel):
    ProductSellableArray: ProductSellableArray | None
    ErrorMessage: base.ErrorMessage | None = None

    @property
    def is_ok(self):
        return self.ErrorMessage is None
