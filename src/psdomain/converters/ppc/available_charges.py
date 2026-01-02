"""
PPC v1.0.0 AvailableCharges converter.

Converts between pydantic AvailableChargesResponse and proto GetAvailableChargesResponse.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.ppc import (
    AvailableChargesResponse,
    AvailableCharge,
    AvailableChargeArray,
    ChargeType,
)
from psdomain.converters.ppc.base import (
    error_message_to_proto,
    error_message_from_proto,
    proto_str_or_none,
    pydantic_str_or_empty,
)

if TYPE_CHECKING:
    from psdomain.proto.ppc import v100_pb2 as proto

__all__ = [
    'available_charge_to_proto',
    'available_charge_from_proto',
    'available_charges_to_proto',
    'available_charges_from_proto',
    'to_proto',
    'from_proto',
]


def available_charge_to_proto(ac: AvailableCharge, proto_module) -> "proto.AvailableCharge":
    """Convert pydantic AvailableCharge to proto AvailableCharge."""
    return proto_module.AvailableCharge(
        charge_id=ac.chargeId,
        charge_name=ac.chargeName,
        charge_description=pydantic_str_or_empty(ac.chargeDescription),
        charge_type=str(ac.chargeType) if ac.chargeType else "",
    )


def available_charge_from_proto(p: "proto.AvailableCharge") -> AvailableCharge:
    """Convert proto AvailableCharge to pydantic AvailableCharge."""
    charge_type = None
    if p.charge_type:
        try:
            charge_type = ChargeType(p.charge_type)
        except ValueError:
            charge_type = p.charge_type
    return AvailableCharge(
        chargeId=p.charge_id,
        chargeName=p.charge_name,
        chargeDescription=proto_str_or_none(p.charge_description),
        chargeType=charge_type,
    )


def available_charges_to_proto(response: AvailableChargesResponse) -> "proto.GetAvailableChargesResponse":
    """Convert pydantic AvailableChargesResponse to proto GetAvailableChargesResponse."""
    from psdomain.proto.ppc import v100_pb2 as proto_module

    result = proto_module.GetAvailableChargesResponse()
    if response.AvailableChargeArray:
        for ac in response.AvailableChargeArray.AvailableCharge:
            result.charges.append(available_charge_to_proto(ac, proto_module))
    if response.ErrorMessage:
        result.error_message.CopyFrom(error_message_to_proto(response.ErrorMessage, proto_module))
    return result


def available_charges_from_proto(proto_msg: "proto.GetAvailableChargesResponse") -> AvailableChargesResponse:
    """Convert proto GetAvailableChargesResponse to pydantic AvailableChargesResponse."""
    charges = None
    if proto_msg.charges:
        charges = AvailableChargeArray(
            AvailableCharge=[available_charge_from_proto(ac) for ac in proto_msg.charges]
        )

    error_msg = None
    if proto_msg.HasField('error_message'):
        error_msg = error_message_from_proto(proto_msg.error_message)

    return AvailableChargesResponse(
        AvailableChargeArray=charges,
        ErrorMessage=error_msg,
    )


# Convenience aliases
to_proto = available_charges_to_proto
from_proto = available_charges_from_proto
