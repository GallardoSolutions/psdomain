"""
Order Shipment Notification v1.0.0 converters.

Converts between pydantic GetOrderShipmentNotificationResponse and proto
GetOrderShipmentNotificationResponseV100.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty
from psdomain.model.base import ErrorMessage
from psdomain.model.osn.common import DimUOM, ShipmentDestinationType, WeightUOM
from psdomain.model.osn.v_1_0_0 import (
    Address,
    GetOrderShipmentNotificationResponse,
    Item,
    ItemArray,
    OrderShipmentNotification,
    OrderShipmentNotificationArray,
    Package,
    PackageArray,
    SalesOrder,
    SalesOrderArray,
    ShipmentLocation,
    ShipmentLocationArray,
)

if TYPE_CHECKING:
    from psdomain.proto.osn import osn_pb2 as proto


def _get_proto():
    """Lazy import of proto module."""
    from psdomain.proto.osn import osn_pb2
    return osn_pb2


# --- Timestamp helpers ---


def _get_timestamp_class():
    """Lazy import of Timestamp class."""
    from google.protobuf.timestamp_pb2 import Timestamp
    return Timestamp


def datetime_to_proto(dt: datetime | None):
    """Convert datetime to proto Timestamp."""
    if dt is None:
        return None
    Timestamp = _get_timestamp_class()
    ts = Timestamp()
    ts.FromDatetime(dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc))
    return ts


def datetime_from_proto(ts) -> datetime | None:
    """Convert proto Timestamp to datetime."""
    if ts is None:
        return None
    try:
        return ts.ToDatetime(tzinfo=timezone.utc)
    except Exception:
        return None


# --- Address converters ---


def address_to_proto(addr: Address) -> "proto.AddressV100":
    """Convert pydantic Address to proto AddressV100."""
    pb2 = _get_proto()
    return pb2.AddressV100(
        address1=pydantic_str_or_empty(addr.address1),
        address2=pydantic_str_or_empty(addr.address2),
        address3=pydantic_str_or_empty(addr.address3),
        address4=pydantic_str_or_empty(addr.address4),
        city=pydantic_str_or_empty(addr.city),
        region=pydantic_str_or_empty(addr.region),
        postal_code=pydantic_str_or_empty(addr.postalCode),
        country=pydantic_str_or_empty(addr.country),
    )


def address_from_proto(p: "proto.AddressV100") -> Address:
    """Convert proto AddressV100 to pydantic Address."""
    return Address(
        address1=proto_str_or_none(p.address1),
        address2=proto_str_or_none(p.address2) if p.HasField("address2") else None,
        address3=proto_str_or_none(p.address3) if p.HasField("address3") else None,
        address4=proto_str_or_none(p.address4) if p.HasField("address4") else None,
        city=proto_str_or_none(p.city),
        region=proto_str_or_none(p.region),
        postalCode=proto_str_or_none(p.postal_code),
        country=proto_str_or_none(p.country) if p.HasField("country") else None,
    )


# --- Item converters ---


def item_to_proto(item: Item) -> "proto.ItemV100":
    """Convert pydantic Item to proto ItemV100."""
    pb2 = _get_proto()
    result = pb2.ItemV100(
        supplier_product_id=pydantic_str_or_empty(item.supplierProductId),
        supplier_part_id=pydantic_str_or_empty(item.supplierPartId),
        distributor_product_id=pydantic_str_or_empty(item.distributorProductId),
        distributor_part_id=pydantic_str_or_empty(item.distributorPartId),
    )
    if item.purchaseOrderLineNumber is not None:
        result.purchase_order_line_number = str(item.purchaseOrderLineNumber)
    if item.quantity is not None:
        result.quantity = item.quantity
    return result


def item_from_proto(p: "proto.ItemV100") -> Item:
    """Convert proto ItemV100 to pydantic Item."""
    po_line = None
    if p.HasField("purchase_order_line_number"):
        try:
            po_line = int(p.purchase_order_line_number)
        except (ValueError, TypeError):
            po_line = None

    quantity = None
    if p.HasField("quantity"):
        quantity = p.quantity

    return Item(
        supplierProductId=(
            proto_str_or_none(p.supplier_product_id) if p.HasField("supplier_product_id") else None
        ),
        supplierPartId=proto_str_or_none(p.supplier_part_id) if p.HasField("supplier_part_id") else None,
        distributorProductId=(
            proto_str_or_none(p.distributor_product_id) if p.HasField("distributor_product_id") else None
        ),
        distributorPartId=(
            proto_str_or_none(p.distributor_part_id) if p.HasField("distributor_part_id") else None
        ),
        purchaseOrderLineNumber=po_line,
        quantity=quantity,
    )


# --- Package converters ---


def package_to_proto(pkg: Package) -> "proto.PackageV100":
    """Convert pydantic Package to proto PackageV100."""
    pb2 = _get_proto()
    result = pb2.PackageV100(
        tracking_number=pydantic_str_or_empty(pkg.trackingNumber),
    )

    if pkg.id is not None:
        result.id = pkg.id

    if pkg.shipmentDate:
        ts = datetime_to_proto(pkg.shipmentDate)
        if ts:
            result.shipment_date.CopyFrom(ts)

    if pkg.dimUOM:
        result.dim_uom = pkg.dimUOM.value
    if pkg.length is not None:
        result.length = pkg.length
    if pkg.width is not None:
        result.width = pkg.width
    if pkg.height is not None:
        result.height = pkg.height
    if pkg.weightUOM:
        result.weight_uom = pkg.weightUOM.value
    if pkg.weight is not None:
        result.weight = pkg.weight
    if pkg.carrier:
        result.carrier = pkg.carrier
    if pkg.shipmentMethod:
        result.shipment_method = pkg.shipmentMethod
    if pkg.shippingAccount:
        result.shipping_account = pkg.shippingAccount
    if pkg.shipmentTerms:
        result.shipment_terms = pkg.shipmentTerms

    if pkg.ItemArray and pkg.ItemArray.Item:
        for item in pkg.ItemArray.Item:
            result.items.append(item_to_proto(item))

    return result


def package_from_proto(p: "proto.PackageV100") -> Package:
    """Convert proto PackageV100 to pydantic Package."""
    pkg_id = None
    if p.HasField("id"):
        pkg_id = int(p.id)

    shipment_date = datetime_from_proto(p.shipment_date)
    # shipmentDate is required, so ensure we have a fallback
    if shipment_date is None:
        shipment_date = datetime.now(tz=timezone.utc)

    dim_uom = None
    if p.HasField("dim_uom") and p.dim_uom:
        try:
            dim_uom = DimUOM(p.dim_uom)
        except ValueError:
            dim_uom = None

    weight_uom = None
    if p.HasField("weight_uom") and p.weight_uom:
        try:
            weight_uom = WeightUOM(p.weight_uom)
        except ValueError:
            weight_uom = None

    items = None
    if p.items:
        items = ItemArray(Item=[item_from_proto(i) for i in p.items])

    return Package(
        id=pkg_id,
        trackingNumber=p.tracking_number,
        shipmentDate=shipment_date,
        dimUOM=dim_uom,
        length=p.length if p.HasField("length") else None,
        width=p.width if p.HasField("width") else None,
        height=p.height if p.HasField("height") else None,
        weightUOM=weight_uom,
        weight=p.weight if p.HasField("weight") else None,
        carrier=proto_str_or_none(p.carrier) if p.HasField("carrier") else None,
        shipmentMethod=proto_str_or_none(p.shipment_method) if p.HasField("shipment_method") else None,
        shippingAccount=proto_str_or_none(p.shipping_account) if p.HasField("shipping_account") else None,
        shipmentTerms=proto_str_or_none(p.shipment_terms) if p.HasField("shipment_terms") else None,
        ItemArray=items,
    )


# --- ShipmentLocation converters ---


def shipment_location_to_proto(loc: ShipmentLocation) -> "proto.ShipmentLocationV100":
    """Convert pydantic ShipmentLocation to proto ShipmentLocationV100."""
    pb2 = _get_proto()
    result = pb2.ShipmentLocationV100(
        complete=loc.complete,
    )

    if loc.id is not None:
        result.id = loc.id

    if loc.ShipFromAddress:
        result.ship_from_address.CopyFrom(address_to_proto(loc.ShipFromAddress))

    if loc.ShipToAddress:
        result.ship_to_address.CopyFrom(address_to_proto(loc.ShipToAddress))

    if loc.shipmentDestinationType:
        result.shipment_destination_type = loc.shipmentDestinationType.value

    if loc.PackageArray and loc.PackageArray.Package:
        for pkg in loc.PackageArray.Package:
            result.packages.append(package_to_proto(pkg))

    return result


def shipment_location_from_proto(p: "proto.ShipmentLocationV100") -> ShipmentLocation:
    """Convert proto ShipmentLocationV100 to pydantic ShipmentLocation."""
    loc_id = None
    if p.HasField("id"):
        loc_id = int(p.id)

    ship_from = address_from_proto(p.ship_from_address) if p.HasField("ship_from_address") else Address(
        address1=None, address2=None, address3=None, address4=None,
        city=None, region=None, postalCode=None, country=None
    )

    ship_to = address_from_proto(p.ship_to_address) if p.HasField("ship_to_address") else Address(
        address1=None, address2=None, address3=None, address4=None,
        city=None, region=None, postalCode=None, country=None
    )

    dest_type = None
    if p.HasField("shipment_destination_type") and p.shipment_destination_type:
        try:
            dest_type = ShipmentDestinationType(p.shipment_destination_type)
        except ValueError:
            dest_type = None

    packages = None
    if p.packages:
        packages = PackageArray(Package=[package_from_proto(pkg) for pkg in p.packages])

    return ShipmentLocation(
        id=loc_id,
        complete=p.complete,
        ShipFromAddress=ship_from,
        ShipToAddress=ship_to,
        shipmentDestinationType=dest_type,
        PackageArray=packages,
    )


# --- SalesOrder converters ---


def sales_order_to_proto(so: SalesOrder) -> "proto.SalesOrderV100":
    """Convert pydantic SalesOrder to proto SalesOrderV100."""
    pb2 = _get_proto()
    result = pb2.SalesOrderV100(
        sales_order_number=pydantic_str_or_empty(so.salesOrderNumber),
        complete=so.complete,
    )

    if so.ShipmentLocationArray and so.ShipmentLocationArray.ShipmentLocation:
        for loc in so.ShipmentLocationArray.ShipmentLocation:
            result.shipment_locations.append(shipment_location_to_proto(loc))

    return result


def sales_order_from_proto(p: "proto.SalesOrderV100") -> SalesOrder:
    """Convert proto SalesOrderV100 to pydantic SalesOrder."""
    locations = ShipmentLocationArray(ShipmentLocation=[])
    if p.shipment_locations:
        locations = ShipmentLocationArray(
            ShipmentLocation=[shipment_location_from_proto(loc) for loc in p.shipment_locations]
        )

    return SalesOrder(
        salesOrderNumber=p.sales_order_number,
        complete=p.complete,
        ShipmentLocationArray=locations,
    )


# --- OrderShipmentNotification converters ---


def osn_to_proto(osn: OrderShipmentNotification) -> "proto.OrderShipmentNotificationV100":
    """Convert pydantic OrderShipmentNotification to proto OrderShipmentNotificationV100."""
    pb2 = _get_proto()
    result = pb2.OrderShipmentNotificationV100(
        purchase_order_number=pydantic_str_or_empty(osn.purchaseOrderNumber),
        complete=osn.complete,
    )

    if osn.SalesOrderArray and osn.SalesOrderArray.SalesOrder:
        for so in osn.SalesOrderArray.SalesOrder:
            result.sales_orders.append(sales_order_to_proto(so))

    return result


def osn_from_proto(p: "proto.OrderShipmentNotificationV100") -> OrderShipmentNotification:
    """Convert proto OrderShipmentNotificationV100 to pydantic OrderShipmentNotification."""
    sales_orders = None
    if p.sales_orders:
        sales_orders = SalesOrderArray(
            SalesOrder=[sales_order_from_proto(so) for so in p.sales_orders]
        )

    return OrderShipmentNotification(
        purchaseOrderNumber=p.purchase_order_number,
        complete=p.complete,
        SalesOrderArray=sales_orders,
    )


# --- Main response converters ---


def to_proto(
    response: GetOrderShipmentNotificationResponse,
) -> "proto.GetOrderShipmentNotificationResponseV100":
    """Convert pydantic GetOrderShipmentNotificationResponse to proto GetOrderShipmentNotificationResponseV100."""
    pb2 = _get_proto()
    result = pb2.GetOrderShipmentNotificationResponseV100()

    if response.OrderShipmentNotificationArray and response.OrderShipmentNotificationArray.OrderShipmentNotification:
        for osn in response.OrderShipmentNotificationArray.OrderShipmentNotification:
            result.order_shipment_notifications.append(osn_to_proto(osn))

    if response.ErrorMessage:
        if isinstance(response.ErrorMessage, ErrorMessage):
            result.error_message = pydantic_str_or_empty(response.ErrorMessage.description)
        else:
            result.error_message = str(response.ErrorMessage)

    return result


def from_proto(
    proto_msg: "proto.GetOrderShipmentNotificationResponseV100",
) -> GetOrderShipmentNotificationResponse:
    """Convert proto GetOrderShipmentNotificationResponseV100 to pydantic GetOrderShipmentNotificationResponse."""
    osn_array = None
    if proto_msg.order_shipment_notifications:
        osn_array = OrderShipmentNotificationArray(
            OrderShipmentNotification=[
                osn_from_proto(osn) for osn in proto_msg.order_shipment_notifications
            ]
        )

    error_message = None
    if proto_msg.HasField("error_message") and proto_msg.error_message:
        error_message = ErrorMessage(description=proto_msg.error_message)

    return GetOrderShipmentNotificationResponse(
        OrderShipmentNotificationArray=osn_array,
        ErrorMessage=error_message,
    )
