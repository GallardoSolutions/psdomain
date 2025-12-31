"""
Remittance Advice Service Models

Pydantic models for the PromoStandards Remittance Advice service.
"""
from __future__ import annotations

from pydantic import Field

from .base import PSBaseModel, ServiceMessage


class PayerDetails(PSBaseModel):
    """Payer information for a remittance."""
    payer_name: str | None = None
    email: str | None = None
    phone: str | None = None


class PaymentDetails(PSBaseModel):
    """Payment details for a remittance."""
    amount_paid: float | None = None
    payment_reference_number: str | None = None
    payment_date: str | None = None
    payment_memo: str | None = None
    payment_method: str | None = None


class RemittanceDetail(PSBaseModel):
    """Individual remittance line item."""
    reference_number: str | None = None
    reference_number_type: str | None = None
    credit_memo_number: str | None = None
    amount: float | None = None


class Remittance(PSBaseModel):
    """Main remittance model containing all payment information."""
    currency: str | None = None
    remittance_details: list[RemittanceDetail] = Field(default_factory=list)
    payer_details: PayerDetails | None = None
    payment_details: PaymentDetails | None = None


# Response models

class SendRemittanceAdviceResponse(PSBaseModel):
    """Response for SendRemittanceAdvice endpoint."""
    transaction_id: str | None = None
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetServiceMethodsResponse(PSBaseModel):
    """Response for GetServiceMethods endpoint."""
    service_methods: list[str] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)
