"""
Converters for Pydantic <-> Proto bidirectional conversion.

Usage:
    from psdomain.converters.inventory import v200 as inv_conv
    proto = inv_conv.to_proto(pydantic_model)
    pydantic = inv_conv.from_proto(proto_msg)

Or use convenience imports:
    from psdomain.converters import inventory_v200_to_proto, inventory_v200_from_proto
"""
from .base import snake_to_camel, camel_to_snake, convert_list

__all__ = [
    'snake_to_camel',
    'camel_to_snake',
    'convert_list',
]
