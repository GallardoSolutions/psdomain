"""
PPC v1.0.0 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.ppc import v100 as ppc_conv

    # Pydantic -> Proto
    proto_response = ppc_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = ppc_conv.from_proto(proto_response)
"""
from __future__ import annotations

# Re-export all public functions for backwards compatibility
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
)

from psdomain.converters.ppc.fob_points import (
    fob_point_to_proto,
    fob_point_from_proto,
    fob_points_to_proto,
    fob_points_from_proto,
)

from psdomain.converters.ppc.decoration_colors import (
    color_to_proto,
    color_from_proto,
    decoration_method_to_proto,
    decoration_method_from_proto,
    decoration_colors_to_proto,
    decoration_colors_from_proto,
    decoration_colors_response_to_proto,
    decoration_colors_response_from_proto,
)

from psdomain.converters.ppc.available_locations import (
    available_location_to_proto,
    available_location_from_proto,
    available_locations_to_proto,
    available_locations_from_proto,
)

from psdomain.converters.ppc.available_charges import (
    available_charge_to_proto,
    available_charge_from_proto,
    available_charges_to_proto,
    available_charges_from_proto,
)

from psdomain.converters.ppc.configuration_and_pricing import (
    charge_price_to_proto,
    charge_price_from_proto,
    charge_to_proto,
    charge_from_proto,
    decoration_to_proto,
    decoration_from_proto,
    location_to_proto,
    location_from_proto,
    part_price_to_proto,
    part_price_from_proto,
    part_to_proto,
    part_from_proto,
    fob_to_proto,
    fob_from_proto,
    configuration_to_proto,
    configuration_from_proto,
    config_and_pricing_to_proto,
    config_and_pricing_from_proto,
)

# Define __all__ for explicit public API
__all__ = [
    # Base
    "error_message_to_proto",
    "error_message_from_proto",
    # FobPoints
    "fob_point_to_proto",
    "fob_point_from_proto",
    "fob_points_to_proto",
    "fob_points_from_proto",
    # DecorationColors
    "color_to_proto",
    "color_from_proto",
    "decoration_method_to_proto",
    "decoration_method_from_proto",
    "decoration_colors_to_proto",
    "decoration_colors_from_proto",
    "decoration_colors_response_to_proto",
    "decoration_colors_response_from_proto",
    # AvailableLocations
    "available_location_to_proto",
    "available_location_from_proto",
    "available_locations_to_proto",
    "available_locations_from_proto",
    # AvailableCharges
    "available_charge_to_proto",
    "available_charge_from_proto",
    "available_charges_to_proto",
    "available_charges_from_proto",
    # ConfigurationAndPricing
    "charge_price_to_proto",
    "charge_price_from_proto",
    "charge_to_proto",
    "charge_from_proto",
    "decoration_to_proto",
    "decoration_from_proto",
    "location_to_proto",
    "location_from_proto",
    "part_price_to_proto",
    "part_price_from_proto",
    "part_to_proto",
    "part_from_proto",
    "fob_to_proto",
    "fob_from_proto",
    "configuration_to_proto",
    "configuration_from_proto",
    "config_and_pricing_to_proto",
    "config_and_pricing_from_proto",
]
