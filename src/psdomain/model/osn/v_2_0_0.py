from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, Field

from .. import base
from .common import ShipmentDestinationType, PreProductionProofType, DimUOM, WeightUOM, TRACKING_URLS


class ShippingContactDetails(base.PSBaseModel):
    """A shipment's ship-from or ship-to address, as the supplier sent it.

    Every field is optional and no length or code list is enforced: this is supplier data we pass on, and
    rejecting it fails the whole response (Lincoln Line sends no ship-from postalCode and attentionTo values
    longer than the spec's 35 characters). Same reasoning as 1.0.0's Address.
    """
    attentionTo: str | None = None
    companyName: str | None = None
    address1: str | None = None
    address2: str | None = None
    address3: str | None = None
    city: str | None = None
    region: str | None = None
    postalCode: str | None = None
    country: str | None = None
    email: str | None = None
    phone: str | None = None


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
    # The 2.0.0 schema spells it Quantity; the model keeps 1.0.0's name, and that spelling wins if both come.
    quantity: base.Quantity = Field(validation_alias=AliasChoices('quantity', 'Quantity'))


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

    @property
    def carrier(self):
        if self.FreightDetails.carrier:
            return self.FreightDetails.carrier
        return None

    @property
    def tracking_url(self):
        if not self.trackingNumber or not self.carrier:
            return None

        carrier = self.carrier.upper().strip()

        for key, url_template in TRACKING_URLS.items():
            if key in carrier:
                return url_template.format(self.trackingNumber)

        return None  # Unknown carrier → no link


class PackageArray(base.PSBaseModel):
    Package: list[Package]


type = NullablePackageArray = PackageArray | None


class Shipment(base.PSBaseModel):
    destinationShippedInFull: bool
    customerPickup: bool
    # The 2.0.0 schema spells them shipFromAddress and shipToAddress; the model keeps 1.0.0's names in its
    # output, and those win when a supplier sends both.
    ShipFromAddress: ShippingContactDetails = Field(
        validation_alias=AliasChoices('ShipFromAddress', 'shipFromAddress'))
    ShipToAddress: ShippingContactDetails = Field(
        validation_alias=AliasChoices('ShipToAddress', 'shipToAddress'))
    shipmentDestinationType: ShipmentDestinationType | None
    PackageArray: NullablePackageArray = Field(
        default=None,
        description='An Array of Shipment Packages',
    )


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


type NullableOrderShipmentNotificationArray = OrderShipmentNotificationArray | None


class GetOrderShipmentNotificationResponseV200(base.PSBaseModel):
    OrderShipmentNotificationArray: NullableOrderShipmentNotificationArray = Field(
        default=None,
        description='An Array of OrderShipment Notifications',
    )
    ServiceMessageArray: base.NullableServiceMessageArray = Field(
        default=None,
        description='An Array of Service Messages',
    )
