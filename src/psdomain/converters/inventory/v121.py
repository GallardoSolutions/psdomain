"""
Inventory v1.2.1 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.inventory import v121 as inv_conv

    # Pydantic -> Proto
    proto_response = inv_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = inv_conv.from_proto(proto_response)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.inventory.v_1_2_1 import (
    InventoryLevelsResponseV121,
    ProductVariationInventory,
    ProductVariationInventoryArray,
    ProductCompanionInventory,
    ProductCompanionInventoryArray,
    AttributeFlex,
    AttributeFlexArray,
)
from psdomain.converters.base import proto_str_or_none

if TYPE_CHECKING:
    from psdomain.proto.inventory import v121_pb2 as proto


# --- AttributeFlex converters ---

def attribute_flex_to_proto(af: AttributeFlex, proto_module) -> 'proto.AttributeFlex':
    """Convert pydantic AttributeFlex to proto AttributeFlex."""
    return proto_module.AttributeFlex(
        id=af.id,
        name=af.name,
        value=af.value
    )


def attribute_flex_from_proto(p) -> AttributeFlex:
    """Convert proto AttributeFlex to pydantic AttributeFlex."""
    return AttributeFlex(
        id=p.id,
        name=p.name,
        value=p.value
    )


# --- ProductVariationInventory converters ---

def product_variation_to_proto(pv: ProductVariationInventory, proto_module) -> 'proto.ProductVariationInventory':
    """Convert pydantic ProductVariationInventory to proto ProductVariationInventory."""
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.ProductVariationInventory(
        part_id=pv.partID,
        quantity_available=int(pv.quantityAvailable) if pv.quantityAvailable else 0,
    )

    if pv.partDescription:
        result.part_description = pv.partDescription
    if pv.partBrand:
        result.part_brand = pv.partBrand
    if pv.priceVariance:
        result.price_variance = pv.priceVariance
    if pv.attributeColor:
        result.attribute_color = pv.attributeColor
    if pv.attributeSize:
        result.attribute_size = pv.attributeSize
    if pv.attributeSelection:
        result.attribute_selection = pv.attributeSelection
    if pv.customProductMessage:
        result.custom_product_message = pv.customProductMessage
    if pv.entryType:
        result.entry_type = pv.entryType

    if pv.AttributeFlexArray:
        for af in pv.AttributeFlexArray.AttributeFlex:
            result.flex_attributes.append(attribute_flex_to_proto(af, proto_module))

    if pv.validTimestamp:
        ts = Timestamp()
        ts.FromDatetime(pv.validTimestamp)
        result.valid_timestamp.CopyFrom(ts)

    return result


def product_variation_from_proto(p) -> ProductVariationInventory:
    """Convert proto ProductVariationInventory to pydantic ProductVariationInventory."""
    flex_array = None
    if p.flex_attributes:
        flex_array = AttributeFlexArray(
            AttributeFlex=[attribute_flex_from_proto(af) for af in p.flex_attributes]
        )

    valid_timestamp = None
    if p.HasField('valid_timestamp'):
        valid_timestamp = p.valid_timestamp.ToDatetime()

    return ProductVariationInventory(
        partID=p.part_id,
        partDescription=proto_str_or_none(p.part_description) if p.HasField('part_description') else None,
        partBrand=proto_str_or_none(p.part_brand) if p.HasField('part_brand') else None,
        priceVariance=proto_str_or_none(p.price_variance) if p.HasField('price_variance') else None,
        quantityAvailable=str(p.quantity_available),
        attributeColor=proto_str_or_none(p.attribute_color) if p.HasField('attribute_color') else None,
        attributeSize=proto_str_or_none(p.attribute_size) if p.HasField('attribute_size') else None,
        attributeSelection=(
            proto_str_or_none(p.attribute_selection) if p.HasField('attribute_selection') else None
        ),
        AttributeFlexArray=flex_array,
        customProductMessage=(
            proto_str_or_none(p.custom_product_message) if p.HasField('custom_product_message') else None
        ),
        entryType=proto_str_or_none(p.entry_type) if p.HasField('entry_type') else None,
        validTimestamp=valid_timestamp,
    )


# --- ProductCompanionInventory converters ---

def product_companion_to_proto(pc: ProductCompanionInventory, proto_module) -> 'proto.ProductCompanionInventory':
    """Convert pydantic ProductCompanionInventory to proto ProductCompanionInventory."""
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.ProductCompanionInventory(
        part_id=pc.partID,
        quantity_available=int(pc.quantityAvailable) if pc.quantityAvailable else 0,
    )

    if pc.partDescription:
        result.part_description = pc.partDescription
    if pc.partBrand:
        result.part_brand = pc.partBrand
    if pc.price:
        result.price = pc.price
    if pc.attributeColor:
        result.attribute_color = pc.attributeColor
    if pc.attributeSize:
        result.attribute_size = pc.attributeSize
    if pc.attributeSelection:
        result.attribute_selection = pc.attributeSelection
    if pc.entryType:
        result.entry_type = pc.entryType
    if pc.customProductMessage:
        result.custom_product_message = pc.customProductMessage

    if pc.AttributeFlexArray:
        for af in pc.AttributeFlexArray.AttributeFlex:
            result.flex_attributes.append(attribute_flex_to_proto(af, proto_module))

    if pc.validTimestamp:
        ts = Timestamp()
        ts.FromDatetime(pc.validTimestamp)
        result.valid_timestamp.CopyFrom(ts)

    return result


def product_companion_from_proto(p) -> ProductCompanionInventory:
    """Convert proto ProductCompanionInventory to pydantic ProductCompanionInventory."""
    flex_array = None
    if p.flex_attributes:
        flex_array = AttributeFlexArray(
            AttributeFlex=[attribute_flex_from_proto(af) for af in p.flex_attributes]
        )

    valid_timestamp = None
    if p.HasField('valid_timestamp'):
        valid_timestamp = p.valid_timestamp.ToDatetime()

    return ProductCompanionInventory(
        partID=p.part_id,
        partDescription=proto_str_or_none(p.part_description) if p.HasField('part_description') else None,
        partBrand=proto_str_or_none(p.part_brand) if p.HasField('part_brand') else None,
        price=proto_str_or_none(p.price) if p.HasField('price') else None,
        quantityAvailable=str(p.quantity_available),
        attributeColor=proto_str_or_none(p.attribute_color) if p.HasField('attribute_color') else None,
        attributeSize=proto_str_or_none(p.attribute_size) if p.HasField('attribute_size') else None,
        attributeSelection=(
            proto_str_or_none(p.attribute_selection) if p.HasField('attribute_selection') else None
        ),
        entryType=proto_str_or_none(p.entry_type) if p.HasField('entry_type') else None,
        AttributeFlexArray=flex_array,
        customProductMessage=(
            proto_str_or_none(p.custom_product_message) if p.HasField('custom_product_message') else None
        ),
        validTimestamp=valid_timestamp,
    )


# --- ServiceMessage converters ---

def service_message_to_proto(msg, proto_module):
    """Convert pydantic ServiceMessage to proto ServiceMessage."""
    return proto_module.ServiceMessage(
        code=msg.code,
        description=msg.description,
        severity=str(msg.severity) if msg.severity else ""
    )


def service_message_from_proto(p):
    """Convert proto ServiceMessage to pydantic ServiceMessage."""
    from psdomain.model.base import ServiceMessage
    severity_str = p.severity if p.severity else "Error"
    return ServiceMessage(
        code=p.code,
        description=p.description,
        severity=severity_str
    )


# --- Main Response converters (Public API) ---

def to_proto(response: InventoryLevelsResponseV121):
    """Convert pydantic InventoryLevelsResponseV121 to proto GetInventoryLevelsResponseV121.

    Args:
        response: Pydantic InventoryLevelsResponseV121 model

    Returns:
        Proto GetInventoryLevelsResponseV121 message
    """
    from psdomain.proto.inventory import v121_pb2 as proto_module

    result = proto_module.GetInventoryLevelsResponseV121()

    # Set inventory
    result.inventory.product_id = response.productID

    if response.errorMessage:
        result.inventory.error_message = response.errorMessage

    if response.ProductVariationInventoryArray:
        for pv in response.ProductVariationInventoryArray.ProductVariationInventory:
            result.inventory.product_variations.append(product_variation_to_proto(pv, proto_module))

    if response.ProductCompanionInventoryArray:
        for pc in response.ProductCompanionInventoryArray.ProductCompanionInventory:
            result.inventory.product_companions.append(product_companion_to_proto(pc, proto_module))

    return result


def from_proto(proto_msg) -> InventoryLevelsResponseV121:
    """Convert proto GetInventoryLevelsResponseV121 to pydantic InventoryLevelsResponseV121.

    Args:
        proto_msg: Proto GetInventoryLevelsResponseV121 message

    Returns:
        Pydantic InventoryLevelsResponseV121 model
    """
    product_id = proto_msg.inventory.product_id

    variations = None
    if proto_msg.inventory.product_variations:
        variations = ProductVariationInventoryArray(
            ProductVariationInventory=[
                product_variation_from_proto(pv)
                for pv in proto_msg.inventory.product_variations
            ]
        )

    companions = None
    if proto_msg.inventory.product_companions:
        companions = ProductCompanionInventoryArray(
            ProductCompanionInventory=[
                product_companion_from_proto(pc)
                for pc in proto_msg.inventory.product_companions
            ]
        )

    error_message = None
    if proto_msg.inventory.HasField('error_message'):
        error_message = proto_msg.inventory.error_message

    return InventoryLevelsResponseV121(
        productID=product_id,
        ProductVariationInventoryArray=variations,
        ProductCompanionInventoryArray=companions,
        errorMessage=error_message,
    )
