from .base import ServiceCode, ConfigurationType, PriceType, ALL_SERVICE_CODES
from . import exceptions
from .product_data.common import Product
from .product_data.latest import ProductDateModifiedResponseLatest, ProductCloseOutResponseLatest, ProductLatest, \
    ProductResponseLatest
from .product_data.v_1_0_0 import ProductDateModifiedResponseV100, ProductCloseOutResponseV100, ProductV100, \
    ProductResponseV100, GetProductSellableResponseV100
from .product_data.v_2_0_0 import ProductDateModifiedResponseV200, ProductCloseOutResponseV200, ProductV200, \
    ProductResponseV200, GetProductSellableResponseV200
from .media_content import MediaContent, MediaType, MediaContentArray, MediaContentDetailsResponse, \
    GetMediaDateModifiedResponse
from .ppc import DecorationColorResponse, FobPointArray, LocationArray, AvailableChargesResponse, \
    ConfigurationAndPricingResponse, AvailableLocationsResponse, FobPointsResponse
from .inventory.v_2_0_0 import FilterValuesResponseV200, InventoryLevelsResponseV200, ProductIDType
from .inventory.v_1_2_1 import InventoryLevelsResponseV121
from .order_status.v_1_0_0 import OrderStatusDetailsResponse, QueryType, OrderStatusTypesResponse
from .order_status.v_2_0_0 import GetServiceMethodsResponseV200, GetIssueResponseV200, GetOrderStatusResponseV200

ProductDateModifiedResponse = ProductDateModifiedResponseLatest | ProductDateModifiedResponseV100 | \
                              ProductDateModifiedResponseV200
ProductCloseOutResponse = ProductCloseOutResponseLatest | ProductCloseOutResponseV100 | ProductCloseOutResponseV200

ProductResponse = ProductResponseLatest | ProductResponseV100 | ProductResponseV200
InventoryLevelsResponse = InventoryLevelsResponseV121 | InventoryLevelsResponseV200
GetProductSellableResponse = GetProductSellableResponseV100 | GetProductSellableResponseV200

__all__ = [
    'ServiceCode', 'exceptions', 'ProductResponse', 'MediaContent', 'MediaType', 'QueryType',
    'MediaContentArray', 'GetProductSellableResponse', 'DecorationColorResponse', 'FobPointArray', 'LocationArray',
    'Product', 'AvailableChargesResponse', 'ConfigurationAndPricingResponse', 'ConfigurationType', 'PriceType',
    'AvailableLocationsResponse', 'FobPointsResponse', 'FilterValuesResponseV200', 'InventoryLevelsResponseV200',
    'MediaContentDetailsResponse', 'OrderStatusDetailsResponse', 'OrderStatusTypesResponse', 'ALL_SERVICE_CODES',
    'ProductIDType', 'GetMediaDateModifiedResponse', 'ProductDateModifiedResponseLatest', 'ServiceCode',
    'ProductCloseOutResponseLatest',  'ProductDateModifiedResponseV100', 'ProductV200', 'ProductResponseV200',
    'ProductCloseOutResponseV100', 'ProductDateModifiedResponseV200', 'ProductCloseOutResponseV200',
    'ProductDateModifiedResponse', 'ProductCloseOutResponse', 'ProductLatest', 'ProductResponseLatest',
    'ProductV100', 'ProductResponseV100', 'InventoryLevelsResponse', 'InventoryLevelsResponseV121',
    'GetServiceMethodsResponseV200', 'GetIssueResponseV200', 'GetOrderStatusResponseV200',
    'GetProductSellableResponseV100', 'GetProductSellableResponseV200'
]
