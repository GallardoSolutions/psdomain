"""
Company Data Service Models

Pydantic models for the PromoStandards Company Data service.
"""
from __future__ import annotations

from pydantic import Field

from .base import PSBaseModel, ServiceMessage


class Address(PSBaseModel):
    """Physical address information."""
    address_name: str | None = None
    attention_to: str | None = None
    address1: str | None = None
    address2: str | None = None
    address3: str | None = None
    city: str | None = None
    region: str | None = None
    postal_code: str | None = None
    country: str | None = None


class Phone(PSBaseModel):
    """Phone contact information."""
    phone_type: str | None = None
    phone_number: str | None = None
    phone_extension: str | None = None


class Contact(PSBaseModel):
    """Contact information for a person."""
    contact_name: str | None = None
    contact_department: str | None = None
    contact_role: str | None = None
    contact_title: str | None = None
    physical_location_id: str | None = None
    business_line_id: str | None = None
    phones: list[Phone] = Field(default_factory=list)
    email: str | None = None


class Identifier(PSBaseModel):
    """Business identifier (e.g., tax ID, DUNS number)."""
    identifier_type: str | None = None
    identifier_number: str | None = None
    country: str | None = None
    start_date: str | None = None
    expiry_date: str | None = None


class Brand(PSBaseModel):
    """Brand information."""
    brand_id: str | None = None
    brand_name: str | None = None
    brand_logo_url: str | None = None


class BusinessLine(PSBaseModel):
    """Business line within a company."""
    business_line_id: str | None = None
    name: str | None = None
    website: str | None = None
    logo_url: str | None = None
    contact: Contact | None = None
    identifiers: list[Identifier] = Field(default_factory=list)
    brands: list[Brand] = Field(default_factory=list)


class CompanyData(PSBaseModel):
    """Main company data model."""
    name: str | None = None
    website: str | None = None
    logo_url: str | None = None
    contact: Contact | None = None
    identifiers: list[Identifier] = Field(default_factory=list)
    business_lines: list[BusinessLine] = Field(default_factory=list)


class BusinessCharacteristic(PSBaseModel):
    """Business characteristic or capability."""
    business_characteristic_category: str | None = None
    business_characteristic_name: str | None = None
    business_characteristic_description: str | None = None


class Certification(PSBaseModel):
    """Company certification information."""
    certification_category: str | None = None
    certification_name: str | None = None
    certification_number: str | None = None
    start_date: str | None = None
    expiry_date: str | None = None
    certification_description: str | None = None
    certification_url: str | None = None
    certification_body_url: str | None = None


class PaymentMethod(PSBaseModel):
    """Accepted payment method."""
    payment_method_type: str | None = None
    payment_method_name: str | None = None
    payment_method_description: str | None = None
    payment_method_surcharge: float | None = None


class PaymentTerms(PSBaseModel):
    """Payment terms offered."""
    payment_terms_name: str | None = None
    payment_terms_anchor: str | None = None
    payment_due_days: int | None = None
    payment_discount: float | None = None
    payment_discount_days: int | None = None


class PhysicalLocation(PSBaseModel):
    """Physical location (warehouse, office, etc.)."""
    physical_location_id: str | None = None
    address: Address | None = None
    fob_id: str | None = None
    inventory_location_id: str | None = None
    business_line_id: str | None = None
    default_shipping_method_id: str | None = None


class Policy(PSBaseModel):
    """Company policy information."""
    policy_category: str | None = None
    policy_name: str | None = None
    policy_description: str | None = None
    start_date: str | None = None
    expiry_date: str | None = None


class PromoStandardsService(PSBaseModel):
    """Available PromoStandards service."""
    promo_standards_service_type: str | None = None
    ws_version: str | None = None


class PromoStandardsServiceDetail(PSBaseModel):
    """Detailed PromoStandards service information."""
    promo_standards_service_type: str | None = None
    ws_version: str | None = None
    endpoint_url: str | None = None
    wsdl_url: str | None = None
    environment: str | None = None
    country: str | None = None


class ShippingMethod(PSBaseModel):
    """Shipping method offered."""
    shipping_method_id: str | None = None
    shipping_method_name: str | None = None
    is_default_shipping_method: bool = False
    shipping_method_carrier: str | None = None
    shipping_method_service: str | None = None
    shipping_account_type: str | None = None
    physical_location_ids: list[str] = Field(default_factory=list)


# Response models

class GetCompanyDataResponse(PSBaseModel):
    """Response for GetCompanyData endpoint."""
    company_data: CompanyData | None = None
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetAvailablePromoStandardsServicesResponse(PSBaseModel):
    """Response for GetAvailablePromoStandardsServices endpoint."""
    promo_standards_services: list[PromoStandardsService] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetPromoStandardsServiceDetailsResponse(PSBaseModel):
    """Response for GetPromoStandardsServiceDetails endpoint."""
    promo_standards_service_details: list[PromoStandardsServiceDetail] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetBusinessCharacteristicsResponse(PSBaseModel):
    """Response for GetBusinessCharacteristics endpoint."""
    business_characteristics: list[BusinessCharacteristic] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetCertificationsResponse(PSBaseModel):
    """Response for GetCertifications endpoint."""
    certifications: list[Certification] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetContactsResponse(PSBaseModel):
    """Response for GetContacts endpoint."""
    contacts: list[Contact] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetPaymentMethodsResponse(PSBaseModel):
    """Response for GetPaymentMethods endpoint."""
    payment_methods: list[PaymentMethod] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetPaymentTermsResponse(PSBaseModel):
    """Response for GetPaymentTerms endpoint."""
    payment_terms: list[PaymentTerms] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetPhysicalLocationsResponse(PSBaseModel):
    """Response for GetPhysicalLocations endpoint."""
    physical_locations: list[PhysicalLocation] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetPoliciesResponse(PSBaseModel):
    """Response for GetPolicies endpoint."""
    policies: list[Policy] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetShippingMethodsResponse(PSBaseModel):
    """Response for GetShippingMethods endpoint."""
    shipping_methods: list[ShippingMethod] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)


class GetServiceMethodsResponse(PSBaseModel):
    """Response for GetServiceMethods endpoint."""
    service_methods: list[str] = Field(default_factory=list)
    service_messages: list[ServiceMessage] = Field(default_factory=list)
