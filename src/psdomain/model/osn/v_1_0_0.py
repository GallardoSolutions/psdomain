"""
https://tools.promostandards.org/order-ship-notification-1-0-0
Order Shipment Notification

Summary: Provides a mechanism to get shipment details by specific parameters like
(purchase order number, sales order number, or shipment date).  This allows the consumer of the service to obtain
shipment information grouped by purchase order number and sales order number for their needs.

Function: getOrderShipmentNotification()
"""
from datetime import datetime

from pydantic import Field

from .. import base
from . import common
from .common import ShipmentDestinationType


class Item(base.PSBaseModel):
    supplierProductId: base.String64 | None
    supplierPartId: base.String64 | None
    distributorProductId: base.String64 | None
    distributorPartId: base.String64 | None
    purchaseOrderLineNumber: int | None
    quantity: float | None


class ItemArray(base.PSBaseModel):
    Item: list[Item]


class Package(base.PSBaseModel):
    id: int | None = Field(default=None)
    trackingNumber: base.String128
    shipmentDate: datetime
    dimUOM: common.DimUOM | None
    length: float | None
    width: float | None
    height: float | None
    weightUOM: common.WeightUOM | None
    weight: float | None
    carrier: base.String128 | None
    shipmentMethod: str | None
    shippingAccount: str | None = Field(default=None)
    shipmentTerms: str | None
    ItemArray: ItemArray | None


class PackageArray(base.PSBaseModel):
    Package: list[Package]


class Address(base.PSBaseModel):
    address1: base.String64
    address2: base.String64 | None
    address3: base.String64 | None
    address4: base.String64 | None
    city: base.String64 | None
    region: base.String2 | None
    postalCode: base.String10 | None
    country: base.String128 | None


class ShipmentLocation(base.PSBaseModel):
    id: int | None
    complete: bool
    ShipFromAddress: Address
    ShipToAddress: Address
    shipmentDestinationType: ShipmentDestinationType | None
    PackageArray: PackageArray | None


class ShipmentLocationArray(base.PSBaseModel):
    ShipmentLocation: list[ShipmentLocation]


class SalesOrder(base.PSBaseModel):
    salesOrderNumber: str
    complete: bool
    ShipmentLocationArray: ShipmentLocationArray


class SalesOrderArray(base.PSBaseModel):
    SalesOrder: list[SalesOrder]


class OrderShipmentNotification(base.PSBaseModel):
    purchaseOrderNumber: base.String64
    complete: bool
    SalesOrderArray: SalesOrderArray | None


class OrderShipmentNotificationArray(base.PSBaseModel):
    OrderShipmentNotification: list[OrderShipmentNotification]


class GetOrderShipmentNotificationResponse(base.PSBaseModel):
    """
    Response for the GetOrderShipmentNotification method.
    """
    OrderShipmentNotificationArray: OrderShipmentNotificationArray | None
    ErrorMessage: base.ErrorMessage | None
