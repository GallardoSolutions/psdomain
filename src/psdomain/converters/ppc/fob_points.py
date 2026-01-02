"""
PPC v1.0.0 FobPoints converter.

Converts between pydantic FobPointsResponse and proto GetFobPointsResponse.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.ppc import (
    FobPointsResponse,
    FobPoint,
    FobPointArray,
    CurrencySupported,
    CurrencySupportedArray,
    Product,
    ProductArray,
)
from psdomain.model.base import Currency
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
    proto_str_or_none,
)

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

__all__ = [
    'fob_point_to_proto',
    'fob_point_from_proto',
    'fob_points_to_proto',
    'fob_points_from_proto',
    'to_proto',
    'from_proto',
]


def fob_point_to_proto(fp: FobPoint, proto_module) -> "proto.FobPoint":
    """Convert pydantic FobPoint to proto FobPoint."""
    result = proto_module.FobPoint(
        fob_id=fp.fobId,
    )
    if fp.fobPostalCode:
        result.fob_postal_code = fp.fobPostalCode
    if fp.fobCity:
        result.fob_city = fp.fobCity
    if fp.fobState:
        result.fob_state = fp.fobState
    if fp.fobCountry:
        result.fob_country = fp.fobCountry
    if fp.CurrencySupportedArray:
        for cs in fp.CurrencySupportedArray.CurrencySupported:
            result.currencies_supported.append(str(cs.currency))
    if fp.ProductArray:
        for p in fp.ProductArray.Product:
            result.product_ids.append(p.productId)
    return result


def fob_point_from_proto(p: "proto.FobPoint") -> FobPoint:
    """Convert proto FobPoint to pydantic FobPoint."""
    currencies = None
    if p.currencies_supported:
        currencies = CurrencySupportedArray(
            CurrencySupported=[
                CurrencySupported(currency=Currency(c)) for c in p.currencies_supported
            ]
        )

    products = None
    if p.product_ids:
        products = ProductArray(
            Product=[Product(productId=pid) for pid in p.product_ids]
        )

    return FobPoint(
        fobId=p.fob_id,
        fobPostalCode=proto_str_or_none(p.fob_postal_code) if p.HasField('fob_postal_code') else None,
        fobCity=proto_str_or_none(p.fob_city) if p.HasField('fob_city') else None,
        fobState=proto_str_or_none(p.fob_state) if p.HasField('fob_state') else None,
        fobCountry=proto_str_or_none(p.fob_country) if p.HasField('fob_country') else None,
        CurrencySupportedArray=currencies,
        ProductArray=products,
    )


def fob_points_to_proto(response: FobPointsResponse) -> "proto.GetFobPointsResponse":
    """Convert pydantic FobPointsResponse to proto GetFobPointsResponse."""
    from psdomain.proto.ppc import v100_pb2 as proto_module

    result = proto_module.GetFobPointsResponse()
    if response.FobPointArray:
        for fp in response.FobPointArray.FobPoint:
            result.fob_points.append(fob_point_to_proto(fp, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def fob_points_from_proto(proto_msg: "proto.GetFobPointsResponse") -> FobPointsResponse:
    """Convert proto GetFobPointsResponse to pydantic FobPointsResponse."""
    fob_points = None
    if proto_msg.fob_points:
        fob_points = FobPointArray(FobPoint=[fob_point_from_proto(fp) for fp in proto_msg.fob_points])

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return FobPointsResponse(
        FobPointArray=fob_points,
        ErrorMessage=error_msg,
    )


# Convenience aliases
to_proto = fob_points_to_proto
from_proto = fob_points_from_proto
