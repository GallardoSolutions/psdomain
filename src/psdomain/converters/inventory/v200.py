"""
Inventory v2.0.0 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.inventory import v200 as inv_conv

    # Pydantic -> Proto
    proto_response = inv_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = inv_conv.from_proto(proto_response)
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from psdomain.model.inventory.v_2_0_0 import (
    InventoryLevelsResponseV200,
    FilterValuesResponseV200,
    Inventory,
    PartInventory,
    PartInventoryArray,
    QuantityAvailable,
    Quantity,
    InventoryLocation,
    InventoryLocationArray,
    FutureAvailability,
    FutureAvailabilityArray,
    FilterValues,
    Filter,
    ArrayOfPartId,
    ArrayOfLabelSize,
    ArrayOfPartColor,
)
from psdomain.model.base import (
    ServiceMessageArray,
    ServiceMessage,
)
from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty

if TYPE_CHECKING:
    from psdomain.proto.inventory import v200_pb2 as proto


# --- Quantity converters ---

def quantity_to_proto(qty: Quantity, proto_module) -> 'proto.QuantityAvailable':
    """Convert pydantic Quantity to proto QuantityAvailable."""
    return proto_module.QuantityAvailable(
        value=int(qty.value),
        uom=str(qty.uom) if qty.uom else ""
    )


def quantity_from_proto(p) -> QuantityAvailable:
    """Convert proto QuantityAvailable to pydantic QuantityAvailable."""
    uom = p.uom if p.uom else "EA"  # Default to EA if not specified
    return QuantityAvailable(
        Quantity=Quantity(value=Decimal(p.value), uom=uom)
    )


# --- FutureAvailability converters ---

def future_availability_to_proto(fa: FutureAvailability, proto_module) -> 'proto.FutureAvailability':
    """Convert pydantic FutureAvailability to proto FutureAvailability."""
    from google.protobuf.timestamp_pb2 import Timestamp
    result = proto_module.FutureAvailability(
        quantity_value=int(fa.Quantity.value),
        quantity_uom=str(fa.Quantity.uom) if fa.Quantity.uom else ""
    )
    if fa.availableOn:
        ts = Timestamp()
        ts.FromDatetime(fa.availableOn)
        result.available_on.CopyFrom(ts)
    return result


def future_availability_from_proto(p) -> FutureAvailability:
    """Convert proto FutureAvailability to pydantic FutureAvailability."""
    available_on = None
    if p.HasField('available_on'):
        available_on = p.available_on.ToDatetime()

    uom = p.quantity_uom if p.quantity_uom else "EA"
    return FutureAvailability(
        Quantity=Quantity(value=Decimal(p.quantity_value), uom=uom),
        availableOn=available_on or datetime.now()
    )


# --- InventoryLocation converters ---

def inventory_location_to_proto(loc: InventoryLocation, proto_module) -> 'proto.InventoryLocation':
    """Convert pydantic InventoryLocation to proto InventoryLocation."""
    result = proto_module.InventoryLocation(
        inventory_location_id=loc.inventoryLocationId,
        inventory_location_name=pydantic_str_or_empty(loc.inventoryLocationName),
        postal_code=pydantic_str_or_empty(loc.postalCode),
        country=pydantic_str_or_empty(loc.country),
    )
    if loc.inventoryLocationQuantity:
        result.inventory_location_quantity.CopyFrom(
            quantity_to_proto(loc.inventoryLocationQuantity.Quantity, proto_module)
        )
    if loc.FutureAvailabilityArray:
        for fa in loc.FutureAvailabilityArray.FutureAvailability:
            result.future_availability.append(future_availability_to_proto(fa, proto_module))
    return result


def inventory_location_from_proto(p) -> InventoryLocation:
    """Convert proto InventoryLocation to pydantic InventoryLocation."""
    qty = None
    if p.HasField('inventory_location_quantity'):
        qty = quantity_from_proto(p.inventory_location_quantity)

    future_arr = None
    if p.future_availability:
        future_arr = FutureAvailabilityArray(
            FutureAvailability=[future_availability_from_proto(fa) for fa in p.future_availability]
        )

    return InventoryLocation(
        inventoryLocationId=p.inventory_location_id,
        inventoryLocationName=proto_str_or_none(p.inventory_location_name),
        postalCode=proto_str_or_none(p.postal_code),
        country=proto_str_or_none(p.country),
        inventoryLocationQuantity=qty,
        FutureAvailabilityArray=future_arr,
    )


# --- PartInventory converters ---

def part_inventory_to_proto(pi: PartInventory, proto_module) -> 'proto.PartInventory':
    """Convert pydantic PartInventory to proto PartInventory."""
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.PartInventory(
        part_id=pi.partId,
        main_part=pi.mainPart,
        part_color=pydantic_str_or_empty(pi.partColor),
        label_size=pydantic_str_or_empty(pi.labelSize),
        part_description=pydantic_str_or_empty(pi.partDescription),
        manufactured_item=pi.manufacturedItem,
        buy_to_order=pi.buyToOrder,
        replenishment_lead_time=pi.replenishmentLeadTime or 0,
        attribute_selection=pydantic_str_or_empty(pi.attributeSelection),
    )

    if pi.quantityAvailable:
        result.quantity_available.CopyFrom(
            quantity_to_proto(pi.quantityAvailable.Quantity, proto_module)
        )

    if pi.lastModified:
        ts = Timestamp()
        ts.FromDatetime(pi.lastModified)
        result.last_modified.CopyFrom(ts)

    if pi.InventoryLocationArray:
        for loc in pi.InventoryLocationArray.InventoryLocation:
            result.inventory_locations.append(inventory_location_to_proto(loc, proto_module))

    return result


def part_inventory_from_proto(p) -> PartInventory:
    """Convert proto PartInventory to pydantic PartInventory."""
    qty = None
    if p.HasField('quantity_available'):
        qty = quantity_from_proto(p.quantity_available)

    locations = None
    if p.inventory_locations:
        locations = InventoryLocationArray(
            InventoryLocation=[inventory_location_from_proto(loc) for loc in p.inventory_locations]
        )

    last_modified = None
    if p.HasField('last_modified'):
        last_modified = p.last_modified.ToDatetime()

    return PartInventory(
        partId=p.part_id,
        mainPart=p.main_part,
        partColor=proto_str_or_none(p.part_color),
        labelSize=proto_str_or_none(p.label_size),
        partDescription=proto_str_or_none(p.part_description),
        quantityAvailable=qty,
        manufacturedItem=p.manufactured_item,
        buyToOrder=p.buy_to_order,
        replenishmentLeadTime=p.replenishment_lead_time or None,
        attributeSelection=proto_str_or_none(p.attribute_selection),
        lastModified=last_modified,
        InventoryLocationArray=locations,
    )


# --- ServiceMessage converters ---

def service_message_to_proto(msg: ServiceMessage, shared_proto):
    """Convert pydantic ServiceMessage to proto ServiceMessage."""
    return shared_proto.ServiceMessage(
        code=msg.code,
        description=msg.description,
        severity=str(msg.severity) if msg.severity else ""
    )


def service_message_from_proto(p) -> ServiceMessage:
    """Convert proto ServiceMessage to pydantic ServiceMessage."""
    severity_str = p.severity if p.severity else "Error"
    return ServiceMessage(
        code=p.code,
        description=p.description,
        severity=severity_str
    )


# --- Main Response converters (Public API) ---

def to_proto(response: InventoryLevelsResponseV200):
    """Convert pydantic InventoryLevelsResponseV200 to proto GetInventoryLevelsResponse.

    Args:
        response: Pydantic InventoryLevelsResponseV200 model

    Returns:
        Proto GetInventoryLevelsResponse message
    """
    from psdomain.proto.inventory import v200_pb2 as proto_module
    from psdomain.proto.inventory import shared_pb2 as shared_proto

    result = proto_module.GetInventoryLevelsResponse()

    if response.Inventory:
        result.inventory.product_id = response.Inventory.productId
        for pi in response.Inventory.part_inventory:
            result.inventory.part_inventory.append(part_inventory_to_proto(pi, proto_module))

    if response.ServiceMessageArray:
        for msg in response.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(service_message_to_proto(msg, shared_proto))

    return result


def from_proto(proto_msg) -> InventoryLevelsResponseV200:
    """Convert proto GetInventoryLevelsResponse to pydantic InventoryLevelsResponseV200.

    Args:
        proto_msg: Proto GetInventoryLevelsResponse message

    Returns:
        Pydantic InventoryLevelsResponseV200 model
    """
    inventory = None
    if proto_msg.HasField('inventory'):
        parts = [part_inventory_from_proto(pi) for pi in proto_msg.inventory.part_inventory]
        inventory = Inventory(
            productId=proto_msg.inventory.product_id,
            PartInventoryArray=PartInventoryArray(PartInventory=parts) if parts else PartInventoryArray.empty()
        )

    service_messages = None
    if proto_msg.service_messages:
        msgs = [service_message_from_proto(m) for m in proto_msg.service_messages]
        service_messages = ServiceMessageArray(ServiceMessage=msgs)

    return InventoryLevelsResponseV200(
        Inventory=inventory,
        ServiceMessageArray=service_messages
    )


# --- FilterValues converters ---

def filter_values_to_proto(fv: FilterValues, proto_module):
    """Convert pydantic FilterValues to proto FilterValues."""
    result = proto_module.FilterValues(
        product_id=fv.productId or ""
    )

    if fv.Filter:
        if fv.Filter.partIdArray:
            result.part_ids.extend(fv.Filter.partIdArray.partId)
        if fv.Filter.LabelSizeArray:
            result.label_sizes.extend(fv.Filter.LabelSizeArray.labelSize)
        if fv.Filter.PartColorArray:
            result.part_colors.extend(fv.Filter.PartColorArray.partColor)

    return result


def filter_values_from_proto(p) -> FilterValues:
    """Convert proto FilterValues to pydantic FilterValues."""
    filter_obj = Filter(
        partIdArray=ArrayOfPartId(partId=list(p.part_ids)) if p.part_ids else None,
        LabelSizeArray=ArrayOfLabelSize(labelSize=list(p.label_sizes)) if p.label_sizes else None,
        PartColorArray=ArrayOfPartColor(partColor=list(p.part_colors)) if p.part_colors else None,
    )

    return FilterValues(
        productId=proto_str_or_none(p.product_id),
        Filter=filter_obj
    )


def filter_values_response_to_proto(response: FilterValuesResponseV200):
    """Convert pydantic FilterValuesResponseV200 to proto GetFilterValuesResponse."""
    from psdomain.proto.inventory import v200_pb2 as proto_module
    from psdomain.proto.inventory import shared_pb2 as shared_proto

    result = proto_module.GetFilterValuesResponse()

    if response.FilterValues:
        result.filter_values.CopyFrom(filter_values_to_proto(response.FilterValues, proto_module))

    if response.ServiceMessageArray:
        for msg in response.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(service_message_to_proto(msg, shared_proto))

    return result


def filter_values_response_from_proto(proto_msg) -> FilterValuesResponseV200:
    """Convert proto GetFilterValuesResponse to pydantic FilterValuesResponseV200."""
    filter_values = None
    if proto_msg.HasField('filter_values'):
        filter_values = filter_values_from_proto(proto_msg.filter_values)

    service_messages = None
    if proto_msg.service_messages:
        msgs = [service_message_from_proto(m) for m in proto_msg.service_messages]
        service_messages = ServiceMessageArray(ServiceMessage=msgs)

    return FilterValuesResponseV200(
        FilterValues=filter_values,
        ServiceMessageArray=service_messages
    )
