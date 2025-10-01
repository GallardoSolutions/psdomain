from pydantic import Field

from .. import base, GetProductSellableResponseV100, ProductDateModifiedResponseV100, ProductCloseOutResponseV100
from .common import ProductCloseOutArray, ProductDateModifiedArray, ProductSellableArray, \
    Product, LocationDecorationArray, ProductPriceGroupArray, FobPointArray
from ..base import ServiceMessage, Severity, ServiceMessageArray


class ProductV200(Product):
    LocationDecorationArray: LocationDecorationArray | None
    ProductPriceGroupArray: ProductPriceGroupArray | None
    FobPointArray: FobPointArray | None

    def get_min_qty(self, currency='USD', configuration_type='Decorated'):
        product_price_lst = self.get_product_price_array(currency, configuration_type)
        return product_price_lst[0].quantityMin if product_price_lst else None

    def get_product_price_array(self, currency, configuration_type):
        if self.ProductPriceGroupArray is None:
            return []
        conf_type = configuration_type.lower()
        price_groups = self.ProductPriceGroupArray.ProductPriceGroup
        filtered_by_currency = [pg for pg in price_groups if pg.currency == currency]
        for price_group in filtered_by_currency:
            if price_group.description and conf_type in price_group.description.lower():
                return price_group.prices
        #
        if filtered_by_currency:
            price_group = filtered_by_currency[0]
        elif price_groups:
            price_group = price_groups[0]
        else:
            return []
        return price_group.prices

    @property
    def fob_points(self):
        return self.FobPointArray.FobPoint if self.FobPointArray else []


class ProductResponseV200(base.ServiceMessageResponse):
    Product: ProductV200 | None = Field(None, alias='Product', description='Product Information',
                                        title='ProductV200')


class ProductCloseOutResponseV200(base.ServiceMessageResponse):
    ProductCloseOutArray: ProductCloseOutArray | None

    @classmethod
    def from_v100(cls, v100_response: ProductCloseOutResponseV100) -> 'ProductCloseOutResponseV200':
        """
        Convert a V1.0.0 response to a V2.0.0 response.
        """
        arr = from_error_message_to_service_message_array(v100_response.ErrorMessage)
        return cls(ProductCloseOutArray=v100_response.ProductCloseOutArray, ServiceMessageArray=arr)


class ProductDateModifiedResponseV200(base.ServiceMessageResponse):
    ProductDateModifiedArray: ProductDateModifiedArray | None

    @classmethod
    def from_v100(cls, v100_response: ProductDateModifiedResponseV100) -> 'ProductDateModifiedResponseV200':
        """
        Convert a V1.0.0 response to a V2.0.0 response.
        """
        arr = from_error_message_to_service_message_array(v100_response.ErrorMessage)
        return cls(ProductDateModifiedArray=v100_response.ProductDateModifiedArray, ServiceMessageArray=arr)


class GetProductSellableResponseV200(base.ServiceMessageResponse):
    ProductSellableArray: ProductSellableArray | None

    @classmethod
    def from_v100(cls, v100_response: GetProductSellableResponseV100) -> 'GetProductSellableResponseV200':
        """
        Convert a V1.0.0 response to a V2.0.0 response.
        """
        arr = from_error_message_to_service_message_array(v100_response.ErrorMessage)
        return cls(ProductSellableArray=v100_response.ProductSellableArray, ServiceMessageArray=arr)


def from_error_message_to_service_message_array(error_message: base.ErrorMessage) -> ServiceMessageArray:
    """
    Convert an ErrorMessage to a ServiceMessageArray.
    """
    if error_message is None:
        return None
    #
    service_message = ServiceMessage(
        code=error_message.code,
        description=error_message.description,
        severity=Severity.ERROR
    )
    return ServiceMessageArray(ServiceMessage=[service_message])
