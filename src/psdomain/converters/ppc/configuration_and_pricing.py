"""
PPC v1.0.0 ConfigurationAndPricing converter.

Converts between pydantic ConfigurationAndPricingResponse and proto GetConfigurationAndPricingResponse.
"""
from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from psdomain.model.ppc import (
    ConfigurationAndPricingResponse,
    Configuration,
    Part,
    PartArray,
    PartPrice,
    PartPriceArray,
    Location,
    LocationArray,
    LocationId,
    LocationIdArray,
    Decoration,
    DecorationArray,
    Charge,
    ChargeArray,
    ChargePrice,
    ChargePriceArray,
    ChargeType,
    DecorationGeometryType,
    DecorationUomType,
)
from psdomain.model.base import Fob, FobArray, PriceType, UOM
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
    proto_str_or_none,
    pydantic_str_or_empty,
)

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

__all__ = [
    'charge_price_to_proto',
    'charge_price_from_proto',
    'charge_to_proto',
    'charge_from_proto',
    'decoration_to_proto',
    'decoration_from_proto',
    'location_to_proto',
    'location_from_proto',
    'part_price_to_proto',
    'part_price_from_proto',
    'part_to_proto',
    'part_from_proto',
    'fob_to_proto',
    'fob_from_proto',
    'configuration_to_proto',
    'configuration_from_proto',
    'config_and_pricing_to_proto',
    'config_and_pricing_from_proto',
    'to_proto',
    'from_proto',
]


# --- ChargePrice converters ---

def charge_price_to_proto(cp: ChargePrice, proto_module) -> "proto.ChargePrice":
    """Convert pydantic ChargePrice to proto ChargePrice."""
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.ChargePrice(
        x_min_qty=cp.xMinQty,
        x_uom=str(cp.xUom) if cp.xUom else "",
        y_min_qty=cp.yMinQty,
        y_uom=str(cp.yUom) if cp.yUom else "",
        price=float(cp.price) if cp.price else 0.0,
        repeat_price=float(cp.repeatPrice) if cp.repeatPrice else 0.0,
    )
    if cp.discountCode:
        result.discount_code = cp.discountCode
    if cp.repeatDiscountCode:
        result.repeat_discount_code = cp.repeatDiscountCode
    if cp.priceEffectiveDate:
        ts = Timestamp()
        ts.FromDatetime(cp.priceEffectiveDate)
        result.price_effective_date.CopyFrom(ts)
    if cp.priceExpiryDate:
        ts = Timestamp()
        ts.FromDatetime(cp.priceExpiryDate)
        result.price_expiry_date.CopyFrom(ts)
    return result


def charge_price_from_proto(p: "proto.ChargePrice") -> ChargePrice:
    """Convert proto ChargePrice to pydantic ChargePrice."""
    effective_date = None
    if p.HasField('price_effective_date'):
        effective_date = p.price_effective_date.ToDatetime()

    expiry_date = None
    if p.HasField('price_expiry_date'):
        expiry_date = p.price_expiry_date.ToDatetime()

    x_uom = None
    if p.x_uom:
        try:
            x_uom = UOM(p.x_uom)
        except ValueError:
            x_uom = p.x_uom

    y_uom = None
    if p.y_uom:
        try:
            y_uom = DecorationUomType(p.y_uom)
        except ValueError:
            y_uom = p.y_uom

    return ChargePrice(
        xMinQty=p.x_min_qty,
        xUom=x_uom,
        yMinQty=p.y_min_qty,
        yUom=y_uom,
        price=Decimal(str(p.price)) if p.price else Decimal(0),
        discountCode=proto_str_or_none(p.discount_code) if p.HasField('discount_code') else None,
        repeatPrice=Decimal(str(p.repeat_price)) if p.repeat_price else None,
        repeatDiscountCode=proto_str_or_none(p.repeat_discount_code) if p.HasField('repeat_discount_code') else None,
        priceEffectiveDate=effective_date,
        priceExpiryDate=expiry_date,
    )


# --- Charge converters ---

def charge_to_proto(ch: Charge, proto_module) -> "proto.Charge":
    """Convert pydantic Charge to proto Charge."""
    result = proto_module.Charge(
        charge_id=ch.chargeId,
        charge_name=ch.chargeName,
        charge_description=ch.chargeDescription,
        charge_type=str(ch.chargeType) if ch.chargeType else "",
    )
    if ch.ChargePriceArray:
        for cp in ch.ChargePriceArray.ChargePrice:
            result.charge_prices.append(charge_price_to_proto(cp, proto_module))
    if ch.chargesAppliesLTM is not None:
        result.charges_applies_ltm = ch.chargesAppliesLTM
    if ch.chargesPerLocation is not None:
        result.charges_per_location = ch.chargesPerLocation
    if ch.chargesPerColor is not None:
        result.charges_per_color = ch.chargesPerColor
    return result


def charge_from_proto(p: "proto.Charge") -> Charge:
    """Convert proto Charge to pydantic Charge."""
    charge_type = None
    if p.charge_type:
        try:
            charge_type = ChargeType(p.charge_type)
        except ValueError:
            charge_type = p.charge_type

    charge_prices = None
    if p.charge_prices:
        charge_prices = ChargePriceArray(
            ChargePrice=[charge_price_from_proto(cp) for cp in p.charge_prices]
        )

    return Charge(
        chargeId=p.charge_id,
        chargeName=p.charge_name,
        chargeDescription=p.charge_description,
        chargeType=charge_type,
        ChargePriceArray=charge_prices,
        chargesAppliesLTM=p.charges_applies_ltm if p.HasField('charges_applies_ltm') else None,
        chargesPerLocation=p.charges_per_location if p.HasField('charges_per_location') else None,
        chargesPerColor=p.charges_per_color if p.HasField('charges_per_color') else None,
    )


# --- Decoration converters ---

def decoration_to_proto(dec: Decoration, proto_module) -> "proto.Decoration":
    """Convert pydantic Decoration to proto Decoration."""
    result = proto_module.Decoration(
        decoration_id=dec.decorationId,
        decoration_geometry=str(dec.decorationGeometry) if dec.decorationGeometry else "",
        decoration_uom=str(dec.decorationUom) if dec.decorationUom else "",
    )
    if dec.decorationName:
        result.decoration_name = dec.decorationName
    if dec.decorationHeight is not None:
        result.decoration_height = float(dec.decorationHeight)
    if dec.decorationWidth is not None:
        result.decoration_width = float(dec.decorationWidth)
    if dec.decorationDiameter is not None:
        result.decoration_diameter = float(dec.decorationDiameter)
    if dec.allowSubForDefaultLocation is not None:
        result.allow_sub_for_default_location = dec.allowSubForDefaultLocation
    if dec.allowSubForDefaultMethod is not None:
        result.allow_sub_for_default_method = dec.allowSubForDefaultMethod
    if dec.itemPartQuantityLTM is not None:
        result.item_part_quantity_ltm = dec.itemPartQuantityLTM
    if dec.ChargeArray:
        for ch in dec.ChargeArray.Charge:
            result.charges.append(charge_to_proto(ch, proto_module))
    if dec.decorationUnitsIncluded is not None:
        result.decoration_units_included = dec.decorationUnitsIncluded
    if dec.decorationUnitsIncludedUom:
        result.decoration_units_included_uom = str(dec.decorationUnitsIncludedUom)
    if dec.decorationUnitsMax is not None:
        result.decoration_units_max = dec.decorationUnitsMax
    if dec.defaultDecoration is not None:
        result.default_decoration = dec.defaultDecoration
    if dec.leadTime is not None:
        result.lead_time = dec.leadTime
    if dec.rushLeadTime is not None:
        result.rush_lead_time = dec.rushLeadTime
    return result


def decoration_from_proto(p: "proto.Decoration") -> Decoration:
    """Convert proto Decoration to pydantic Decoration."""
    geometry = None
    if p.decoration_geometry:
        try:
            geometry = DecorationGeometryType(p.decoration_geometry)
        except ValueError:
            geometry = p.decoration_geometry

    uom = None
    if p.decoration_uom:
        try:
            uom = DecorationUomType(p.decoration_uom)
        except ValueError:
            uom = p.decoration_uom

    units_uom = None
    if p.HasField('decoration_units_included_uom') and p.decoration_units_included_uom:
        try:
            units_uom = DecorationUomType(p.decoration_units_included_uom)
        except ValueError:
            units_uom = p.decoration_units_included_uom

    charges = None
    if p.charges:
        charges = ChargeArray(Charge=[charge_from_proto(ch) for ch in p.charges])

    return Decoration(
        decorationId=p.decoration_id,
        decorationName=proto_str_or_none(p.decoration_name) if p.HasField('decoration_name') else None,
        decorationGeometry=geometry,
        decorationHeight=Decimal(str(p.decoration_height)) if p.HasField('decoration_height') else None,
        decorationWidth=Decimal(str(p.decoration_width)) if p.HasField('decoration_width') else None,
        decorationDiameter=Decimal(str(p.decoration_diameter)) if p.HasField('decoration_diameter') else None,
        decorationUom=uom,
        allowSubForDefaultLocation=(
            p.allow_sub_for_default_location if p.HasField('allow_sub_for_default_location') else None
        ),
        allowSubForDefaultMethod=(
            p.allow_sub_for_default_method if p.HasField('allow_sub_for_default_method') else None
        ),
        itemPartQuantityLTM=p.item_part_quantity_ltm if p.HasField('item_part_quantity_ltm') else None,
        ChargeArray=charges,
        decorationUnitsIncluded=p.decoration_units_included if p.HasField('decoration_units_included') else None,
        decorationUnitsIncludedUom=units_uom,
        decorationUnitsMax=p.decoration_units_max if p.HasField('decoration_units_max') else None,
        defaultDecoration=p.default_decoration if p.HasField('default_decoration') else None,
        leadTime=p.lead_time if p.HasField('lead_time') else None,
        rushLeadTime=p.rush_lead_time if p.HasField('rush_lead_time') else None,
    )


# --- Location converters ---

def location_to_proto(loc: Location, proto_module) -> "proto.Location":
    """Convert pydantic Location to proto Location."""
    result = proto_module.Location(
        location_id=loc.locationId,
        location_name=pydantic_str_or_empty(loc.locationName),
        decorations_included=loc.decorationsIncluded,
        default_location=loc.defaultLocation,
        max_decoration=loc.maxDecoration,
        min_decoration=loc.minDecoration,
    )
    if loc.DecorationArray:
        for dec in loc.DecorationArray.Decoration:
            result.decorations.append(decoration_to_proto(dec, proto_module))
    if loc.locationRank is not None:
        result.location_rank = loc.locationRank
    return result


def location_from_proto(p: "proto.Location") -> Location:
    """Convert proto Location to pydantic Location."""
    decorations = None
    if p.decorations:
        decorations = DecorationArray(Decoration=[decoration_from_proto(d) for d in p.decorations])

    return Location(
        locationId=p.location_id,
        locationName=proto_str_or_none(p.location_name),
        DecorationArray=decorations,
        decorationsIncluded=p.decorations_included,
        defaultLocation=p.default_location,
        maxDecoration=p.max_decoration,
        minDecoration=p.min_decoration,
        locationRank=p.location_rank if p.HasField('location_rank') else None,
    )


# --- PartPrice converters ---

def part_price_to_proto(pp: PartPrice, proto_module) -> "proto.PartPrice":
    """Convert pydantic PartPrice to proto PartPrice."""
    from google.protobuf.timestamp_pb2 import Timestamp

    result = proto_module.PartPrice(
        min_quantity=pp.minQuantity,
        price=float(pp.price) if pp.price else 0.0,
        price_uom=str(pp.priceUom) if pp.priceUom else "",
    )
    if pp.discountCode:
        result.discount_code = pp.discountCode
    if pp.priceEffectiveDate:
        ts = Timestamp()
        ts.FromDatetime(pp.priceEffectiveDate)
        result.price_effective_date.CopyFrom(ts)
    if pp.priceExpiryDate:
        ts = Timestamp()
        ts.FromDatetime(pp.priceExpiryDate)
        result.price_expiry_date.CopyFrom(ts)
    return result


def part_price_from_proto(p: "proto.PartPrice") -> PartPrice:
    """Convert proto PartPrice to pydantic PartPrice."""
    effective_date = None
    if p.HasField('price_effective_date'):
        effective_date = p.price_effective_date.ToDatetime()

    expiry_date = None
    if p.HasField('price_expiry_date'):
        expiry_date = p.price_expiry_date.ToDatetime()

    price_uom = None
    if p.price_uom:
        try:
            price_uom = UOM(p.price_uom)
        except ValueError:
            price_uom = p.price_uom

    return PartPrice(
        minQuantity=p.min_quantity,
        discountCode=proto_str_or_none(p.discount_code) if p.HasField('discount_code') else None,
        price=Decimal(str(p.price)) if p.price else Decimal(0),
        priceUom=price_uom,
        priceEffectiveDate=effective_date,
        priceExpiryDate=expiry_date,
    )


# --- Part converters ---

def part_to_proto(part: Part, proto_module) -> "proto.Part":
    """Convert pydantic Part to proto Part."""
    result = proto_module.Part(
        part_id=part.partId,
        part_group=part.partGroup,
        part_group_required=part.partGroupRequired,
        part_group_description=pydantic_str_or_empty(part.partGroupDescription),
        ratio=float(part.ratio) if part.ratio else 1.0,
    )
    if part.partDescription:
        result.part_description = part.partDescription
    if part.PartPriceArray:
        for pp in part.PartPriceArray.PartPrice:
            result.part_prices.append(part_price_to_proto(pp, proto_module))
    if part.nextPartGroup is not None:
        result.next_part_group = part.nextPartGroup
    if part.defaultPart is not None:
        result.default_part = part.defaultPart
    if part.LocationIdArray:
        for lid in part.LocationIdArray.LocationId:
            result.location_ids.append(int(lid.locationId) if isinstance(lid.locationId, str) else lid.locationId)
    return result


def part_from_proto(p: "proto.Part") -> Part:
    """Convert proto Part to pydantic Part."""
    part_prices = None
    if p.part_prices:
        part_prices = PartPriceArray(PartPrice=[part_price_from_proto(pp) for pp in p.part_prices])

    location_ids = None
    if p.location_ids:
        location_ids = LocationIdArray(LocationId=[LocationId(locationId=lid) for lid in p.location_ids])

    return Part(
        partId=p.part_id,
        partDescription=proto_str_or_none(p.part_description) if p.HasField('part_description') else None,
        PartPriceArray=part_prices,
        partGroup=p.part_group,
        nextPartGroup=p.next_part_group if p.HasField('next_part_group') else None,
        partGroupRequired=p.part_group_required,
        partGroupDescription=proto_str_or_none(p.part_group_description),
        ratio=Decimal(str(p.ratio)) if p.ratio else Decimal(1),
        defaultPart=p.default_part if p.HasField('default_part') else None,
        LocationIdArray=location_ids,
    )


# --- Fob converters ---

def fob_to_proto(fob: Fob, proto_module) -> "proto.Fob":
    """Convert pydantic Fob to proto Fob."""
    result = proto_module.Fob(fob_id=fob.fobId)
    if fob.fobPostalCode:
        result.fob_postal_code = fob.fobPostalCode
    return result


def fob_from_proto(p: "proto.Fob") -> Fob:
    """Convert proto Fob to pydantic Fob."""
    return Fob(
        fobId=p.fob_id,
        fobPostalCode=proto_str_or_none(p.fob_postal_code) if p.HasField('fob_postal_code') else None,
    )


# --- Configuration converters ---

def configuration_to_proto(config: Configuration, proto_module) -> "proto.Configuration":
    """Convert pydantic Configuration to proto Configuration."""
    result = proto_module.Configuration(
        product_id=pydantic_str_or_empty(config.productId),
        currency=config.currency,
        price_type=str(config.priceType) if config.priceType else "",
    )
    if config.PartArray:
        for part in config.PartArray.Part:
            result.parts.append(part_to_proto(part, proto_module))
    if config.LocationArray:
        for loc in config.LocationArray.Location:
            result.locations.append(location_to_proto(loc, proto_module))
    if config.FobArray:
        for fob in config.FobArray.Fob:
            result.fobs.append(fob_to_proto(fob, proto_module))
    return result


def configuration_from_proto(p: "proto.Configuration") -> Configuration:
    """Convert proto Configuration to pydantic Configuration."""
    parts = None
    if p.parts:
        parts = PartArray(Part=[part_from_proto(part) for part in p.parts])

    locations = None
    if p.locations:
        locations = LocationArray(Location=[location_from_proto(loc) for loc in p.locations])

    fobs = None
    if p.fobs:
        fobs = FobArray(Fob=[fob_from_proto(fob) for fob in p.fobs])

    price_type = None
    if p.price_type:
        try:
            price_type = PriceType(p.price_type)
        except ValueError:
            price_type = p.price_type

    return Configuration(
        PartArray=parts,
        LocationArray=locations,
        productId=proto_str_or_none(p.product_id),
        currency=p.currency,
        FobArray=fobs,
        priceType=price_type,
    )


# --- Response converters (Public API) ---

def config_and_pricing_to_proto(
    response: ConfigurationAndPricingResponse
) -> "proto.GetConfigurationAndPricingResponse":
    """Convert pydantic ConfigurationAndPricingResponse to proto GetConfigurationAndPricingResponse."""
    from psdomain.proto.ppc import v100_pb2 as proto_module

    result = proto_module.GetConfigurationAndPricingResponse()
    if response.Configuration:
        result.configuration.CopyFrom(configuration_to_proto(response.Configuration, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def config_and_pricing_from_proto(
    proto_msg: "proto.GetConfigurationAndPricingResponse"
) -> ConfigurationAndPricingResponse:
    """Convert proto GetConfigurationAndPricingResponse to pydantic ConfigurationAndPricingResponse."""
    configuration = None
    if proto_msg.HasField('configuration'):
        configuration = configuration_from_proto(proto_msg.configuration)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return ConfigurationAndPricingResponse(
        Configuration=configuration,
        ErrorMessage=error_msg,
    )


# Convenience aliases
to_proto = config_and_pricing_to_proto
from_proto = config_and_pricing_from_proto
