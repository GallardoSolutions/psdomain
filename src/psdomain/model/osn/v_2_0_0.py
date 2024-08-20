from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import constr

from .. import base
from .common import ShipmentDestinationType, PreProductionProofType, DimUOM, WeightUOM


class ShippingContactDetails(base.PSBaseModel):
    attentionTo: Optional[base.String35]
    companyName: Optional[base.String35]
    address1: base.String35
    address2: Optional[base.String35]
    address3: Optional[base.String35]
    city: base.String30
    region: base.String3
    postalCode: base.String10
    country: Optional[base.CountryIso2]
    email: Optional[base.String128]
    phone: Optional[constr(max_length=32)]


class DimensionWeight(base.PSBaseModel):
    weightUOM: WeightUOM | None
    weight: Decimal | None


class DimensionSize(base.PSBaseModel):
    dimUOM: DimUOM
    length: Decimal | None
    width: Decimal | None
    height: Decimal | None


class Dimension(base.PSBaseModel):
    DimensionSize: DimensionSize | None
    DimensionWeight: DimensionWeight | None


class FreightDetails(base.PSBaseModel):
    carrier: base.String64 | None
    service: base.String64 | None


class Item(base.PSBaseModel):
    supplierProductId: base.String64 | None
    supplierPartId: base.String64 | None
    distributorProductId: base.String64 | None
    distributorPartId: base.String64 | None
    purchaseOrderLineNumber: int | None
    quantity: base.Quantity


class ItemArray(base.PSBaseModel):
    Item: list[Item]


class Package(base.PSBaseModel):
    id: int | None
    trackingNumber: base.String128
    shipmentDate: datetime
    Dimension: Dimension | None
    FreightDetails: FreightDetails | None
    shippingAccount: base.String128 | None
    shipmentTerms: base.String128 | None
    ItemArray: ItemArray | None
    preProductionProof: PreProductionProofType | None


class PackageArray(base.PSBaseModel):
    Package: list[Package]


class Shipment(base.PSBaseModel):
    destinationShippedInFull: bool
    customerPickup: bool
    ShipFromAddress: ShippingContactDetails
    ShipToAddress: ShippingContactDetails
    shipmentDestinationType: ShipmentDestinationType | None
    PackageArray: PackageArray | None


class ShipmentArray(base.PSBaseModel):
    Shipment: list[Shipment]


class SalesOrder(base.PSBaseModel):
    salesOrderNumber: base.String64
    salesOrderShippedInFull: bool
    ShipmentArray: ShipmentArray


class SalesOrderArray(base.PSBaseModel):
    SalesOrder: list[SalesOrder]


class OrderShipmentNotification(base.PSBaseModel):
    purchaseOrderNumber: base.String64
    purchaseOrderShippedInFull: bool
    SalesOrderArray: SalesOrderArray


class OrderShipmentNotificationArray(base.PSBaseModel):
    OrderShipmentNotification: list[OrderShipmentNotification]


class GetOrderShipmentNotificationResponseV200(base.PSBaseModel):
    OrderShipmentNotificationArray: OrderShipmentNotificationArray | None
    ServiceMessageArray: base.ServiceMessageArray | None
