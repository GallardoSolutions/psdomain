"""
PPC v1.0.0 shared converter utilities.

Contains common converters used across all PPC response types.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.base import ErrorMessage
from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

# Re-export for convenience
__all__ = [
    'error_message_to_proto',
    'error_message_from_proto',
    'proto_str_or_none',
    'pydantic_str_or_empty',
]


def error_message_to_proto(msg: ErrorMessage, proto_module) -> "proto.ErrorMessage":
    """Convert pydantic ErrorMessage to proto ErrorMessage."""
    return proto_module.ErrorMessage(
        code=msg.code,
        description=msg.description,
    )


def error_message_from_proto(p: "proto.ErrorMessage") -> ErrorMessage:
    """Convert proto ErrorMessage to pydantic ErrorMessage."""
    return ErrorMessage(
        code=p.code,
        description=p.description,
    )
