"""
PPC v1.0.0 AvailableLocations converter.

Converts between pydantic AvailableLocationsResponse and proto GetAvailableLocationsResponse.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.ppc import (
    AvailableLocationsResponse,
    AvailableLocationArray,
)
from psdomain.model.product_data.common import Location as ProductDataLocation
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
    proto_str_or_none,
    pydantic_str_or_empty,
)

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

__all__ = [
    'available_location_to_proto',
    'available_location_from_proto',
    'available_locations_to_proto',
    'available_locations_from_proto',
    'to_proto',
    'from_proto',
]


def available_location_to_proto(loc: ProductDataLocation, proto_module) -> "proto.AvailableLocation":
    """Convert pydantic Location to proto AvailableLocation."""
    return proto_module.AvailableLocation(
        location_id=loc.locationId,
        location_name=pydantic_str_or_empty(loc.locationName),
    )


def available_location_from_proto(p: "proto.AvailableLocation") -> ProductDataLocation:
    """Convert proto AvailableLocation to pydantic Location."""
    return ProductDataLocation(
        locationId=p.location_id,
        locationName=proto_str_or_none(p.location_name),
    )


def available_locations_to_proto(response: AvailableLocationsResponse) -> "proto.GetAvailableLocationsResponse":
    """Convert pydantic AvailableLocationsResponse to proto GetAvailableLocationsResponse."""
    from psdomain.proto.ppc import v100_pb2 as proto_module

    result = proto_module.GetAvailableLocationsResponse()
    if response.AvailableLocationArray:
        for loc in response.AvailableLocationArray.AvailableLocation:
            result.locations.append(available_location_to_proto(loc, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def available_locations_from_proto(proto_msg: "proto.GetAvailableLocationsResponse") -> AvailableLocationsResponse:
    """Convert proto GetAvailableLocationsResponse to pydantic AvailableLocationsResponse."""
    locations = None
    if proto_msg.locations:
        locations = AvailableLocationArray(
            AvailableLocation=[available_location_from_proto(loc) for loc in proto_msg.locations]
        )

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return AvailableLocationsResponse(
        AvailableLocationArray=locations,
        ErrorMessage=error_msg,
    )


# Convenience aliases
to_proto = available_locations_to_proto
from_proto = available_locations_from_proto
