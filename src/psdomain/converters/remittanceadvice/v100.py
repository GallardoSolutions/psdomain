"""
Remittance Advice v1.0.0 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.remittanceadvice import v100 as ra_conv

    # Pydantic -> Proto
    proto_response = ra_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = ra_conv.from_proto(proto_response)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.remittance_advice import (
    PayerDetails,
    PaymentDetails,
    RemittanceDetail,
    Remittance,
    SendRemittanceAdviceResponse,
    GetServiceMethodsResponse,
)
from psdomain.model.base import ServiceMessage
from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty

if TYPE_CHECKING:
    from psdomain.proto.remittanceadvice import remittanceadvice_pb2 as proto


# --- Basic model converters ---

def payer_details_to_proto(pd: PayerDetails, proto_module) -> 'proto.PayerDetails':
    result = proto_module.PayerDetails(
        payer_name=pydantic_str_or_empty(pd.payer_name),
    )
    if pd.email:
        result.email = pd.email
    if pd.phone:
        result.phone = pd.phone
    return result


def payer_details_from_proto(p) -> PayerDetails:
    return PayerDetails(
        payer_name=proto_str_or_none(p.payer_name),
        email=proto_str_or_none(p.email) if p.HasField('email') else None,
        phone=proto_str_or_none(p.phone) if p.HasField('phone') else None,
    )


def payment_details_to_proto(pd: PaymentDetails, proto_module) -> 'proto.PaymentDetails':
    result = proto_module.PaymentDetails(
        amount_paid=pd.amount_paid or 0.0,
        payment_reference_number=pydantic_str_or_empty(pd.payment_reference_number),
        payment_date=pydantic_str_or_empty(pd.payment_date),
        payment_method=pydantic_str_or_empty(pd.payment_method),
    )
    if pd.payment_memo:
        result.payment_memo = pd.payment_memo
    return result


def payment_details_from_proto(p) -> PaymentDetails:
    return PaymentDetails(
        amount_paid=p.amount_paid if p.amount_paid else None,
        payment_reference_number=proto_str_or_none(p.payment_reference_number),
        payment_date=proto_str_or_none(p.payment_date),
        payment_memo=proto_str_or_none(p.payment_memo) if p.HasField('payment_memo') else None,
        payment_method=proto_str_or_none(p.payment_method),
    )


def remittance_detail_to_proto(rd: RemittanceDetail, proto_module) -> 'proto.RemittanceDetail':
    result = proto_module.RemittanceDetail(
        reference_number=pydantic_str_or_empty(rd.reference_number),
        reference_number_type=pydantic_str_or_empty(rd.reference_number_type),
        amount=rd.amount or 0.0,
    )
    if rd.credit_memo_number:
        result.credit_memo_number = rd.credit_memo_number
    return result


def remittance_detail_from_proto(p) -> RemittanceDetail:
    return RemittanceDetail(
        reference_number=proto_str_or_none(p.reference_number),
        reference_number_type=proto_str_or_none(p.reference_number_type),
        credit_memo_number=proto_str_or_none(p.credit_memo_number) if p.HasField('credit_memo_number') else None,
        amount=p.amount if p.amount else None,
    )


def remittance_to_proto(rem: Remittance, proto_module) -> 'proto.Remittance':
    result = proto_module.Remittance(
        currency=pydantic_str_or_empty(rem.currency),
    )
    for rd in rem.remittance_details:
        result.remittance_details.append(remittance_detail_to_proto(rd, proto_module))
    if rem.payer_details:
        result.payer_details.CopyFrom(payer_details_to_proto(rem.payer_details, proto_module))
    if rem.payment_details:
        result.payment_details.CopyFrom(payment_details_to_proto(rem.payment_details, proto_module))
    return result


def remittance_from_proto(p) -> Remittance:
    payer = payer_details_from_proto(p.payer_details) if p.HasField('payer_details') else None
    payment = payment_details_from_proto(p.payment_details) if p.HasField('payment_details') else None
    return Remittance(
        currency=proto_str_or_none(p.currency),
        remittance_details=[remittance_detail_from_proto(rd) for rd in p.remittance_details],
        payer_details=payer,
        payment_details=payment,
    )


# --- ServiceMessage converters ---

def service_message_to_proto(msg: ServiceMessage, proto_module):
    return proto_module.ServiceMessage(
        code=msg.code,
        description=msg.description,
        severity=str(msg.severity) if msg.severity else ""
    )


def service_message_from_proto(p) -> ServiceMessage:
    severity_str = p.severity if p.severity else "Error"
    return ServiceMessage(
        code=p.code,
        description=p.description,
        severity=severity_str
    )


# --- Response converters (Public API) ---

def send_remittance_advice_to_proto(response: SendRemittanceAdviceResponse):
    """Convert pydantic SendRemittanceAdviceResponse to proto."""
    from psdomain.proto.remittanceadvice import remittanceadvice_pb2 as proto_module
    result = proto_module.SendRemittanceAdviceResponse()
    if response.transaction_id:
        result.transaction_id = response.transaction_id
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def send_remittance_advice_from_proto(proto_msg) -> SendRemittanceAdviceResponse:
    """Convert proto SendRemittanceAdviceResponse to pydantic."""
    transaction_id = None
    if proto_msg.HasField('transaction_id'):
        transaction_id = proto_msg.transaction_id
    return SendRemittanceAdviceResponse(
        transaction_id=transaction_id,
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


def get_service_methods_to_proto(response: GetServiceMethodsResponse):
    """Convert pydantic GetServiceMethodsResponse to proto."""
    from psdomain.proto.remittanceadvice import remittanceadvice_pb2 as proto_module
    result = proto_module.GetServiceMethodsResponse()
    result.service_methods.extend(response.service_methods)
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_service_methods_from_proto(proto_msg) -> GetServiceMethodsResponse:
    """Convert proto GetServiceMethodsResponse to pydantic."""
    return GetServiceMethodsResponse(
        service_methods=list(proto_msg.service_methods),
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


# Convenience aliases for main endpoint
to_proto = send_remittance_advice_to_proto
from_proto = send_remittance_advice_from_proto
