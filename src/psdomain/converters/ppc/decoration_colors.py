"""
PPC v1.0.0 DecorationColors converter.

Converts between pydantic DecorationColorResponse and proto GetDecorationColorsResponse.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.ppc import (
    DecorationColorResponse,
    DecorationColors,
    DecorationMethod,
    DecorationMethodArray,
    ColorArray,
)
from psdomain.model.product_data.common import Color
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
    proto_str_or_none,
    pydantic_str_or_empty,
)

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

__all__ = [
    'color_to_proto',
    'color_from_proto',
    'decoration_method_to_proto',
    'decoration_method_from_proto',
    'decoration_colors_to_proto',
    'decoration_colors_from_proto',
    'decoration_colors_response_to_proto',
    'decoration_colors_response_from_proto',
    'to_proto',
    'from_proto',
]


def color_to_proto(c: Color, proto_module) -> "proto.Color":
    """Convert pydantic Color to proto Color."""
    return proto_module.Color(
        color_id=pydantic_str_or_empty(c.colorName),  # Using colorName as color_id
        color_name=pydantic_str_or_empty(c.colorName),
    )


def color_from_proto(p: "proto.Color") -> Color:
    """Convert proto Color to pydantic Color."""
    return Color(
        colorName=proto_str_or_none(p.color_name),
    )


def decoration_method_to_proto(dm: DecorationMethod, proto_module) -> "proto.DecorationMethod":
    """Convert pydantic DecorationMethod to proto DecorationMethod."""
    return proto_module.DecorationMethod(
        decoration_id=dm.decorationId,
        decoration_name=dm.decorationName,
    )


def decoration_method_from_proto(p: "proto.DecorationMethod") -> DecorationMethod:
    """Convert proto DecorationMethod to pydantic DecorationMethod."""
    return DecorationMethod(
        decorationId=p.decoration_id,
        decorationName=p.decoration_name,
    )


def decoration_colors_to_proto(dc: DecorationColors, proto_module) -> "proto.DecorationColors":
    """Convert pydantic DecorationColors to proto DecorationColors."""
    result = proto_module.DecorationColors(
        product_id=dc.productId,
        location_id=dc.locationId,
    )
    if dc.pmsMatch is not None:
        result.pms_match = dc.pmsMatch
    if dc.fullColor is not None:
        result.full_color = dc.fullColor
    if dc.ColorArray:
        for c in dc.ColorArray.Color:
            result.colors.append(color_to_proto(c, proto_module))
    if dc.DecorationMethodArray:
        for dm in dc.DecorationMethodArray.DecorationMethod:
            result.decoration_methods.append(decoration_method_to_proto(dm, proto_module))
    return result


def decoration_colors_from_proto(p: "proto.DecorationColors") -> DecorationColors:
    """Convert proto DecorationColors to pydantic DecorationColors."""
    color_array = None
    if p.colors:
        color_array = ColorArray(Color=[color_from_proto(c) for c in p.colors])

    decoration_methods = None
    if p.decoration_methods:
        decoration_methods = DecorationMethodArray(
            DecorationMethod=[decoration_method_from_proto(dm) for dm in p.decoration_methods]
        )

    return DecorationColors(
        productId=p.product_id,
        locationId=p.location_id,
        pmsMatch=p.pms_match if p.HasField('pms_match') else None,
        fullColor=p.full_color if p.HasField('full_color') else None,
        ColorArray=color_array,
        DecorationMethodArray=decoration_methods,
    )


def decoration_colors_response_to_proto(response: DecorationColorResponse) -> "proto.GetDecorationColorsResponse":
    """Convert pydantic DecorationColorResponse to proto GetDecorationColorsResponse."""
    from psdomain.proto.ppc import v100_pb2 as proto_module

    result = proto_module.GetDecorationColorsResponse()
    if response.DecorationColors:
        result.decoration_colors.CopyFrom(decoration_colors_to_proto(response.DecorationColors, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def decoration_colors_response_from_proto(proto_msg: "proto.GetDecorationColorsResponse") -> DecorationColorResponse:
    """Convert proto GetDecorationColorsResponse to pydantic DecorationColorResponse."""
    decoration_colors = None
    if proto_msg.HasField('decoration_colors'):
        decoration_colors = decoration_colors_from_proto(proto_msg.decoration_colors)

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return DecorationColorResponse(
        DecorationColors=decoration_colors,
        ErrorMessage=error_msg,
    )


# Convenience aliases
to_proto = decoration_colors_response_to_proto
from_proto = decoration_colors_response_from_proto
