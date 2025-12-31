"""
Company Data v1.0.0 Pydantic <-> Proto converters.

Usage:
    from psdomain.converters.companydata import v100 as cd_conv

    # Pydantic -> Proto
    proto_response = cd_conv.to_proto(pydantic_response)

    # Proto -> Pydantic
    pydantic_response = cd_conv.from_proto(proto_response)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from psdomain.model.company_data import (
    Address,
    Phone,
    Contact,
    Identifier,
    Brand,
    BusinessLine,
    CompanyData,
    BusinessCharacteristic,
    Certification,
    PaymentMethod,
    PaymentTerms,
    PhysicalLocation,
    Policy,
    PromoStandardsService,
    PromoStandardsServiceDetail,
    ShippingMethod,
    GetCompanyDataResponse,
    GetAvailablePromoStandardsServicesResponse,
    GetCertificationsResponse,
    GetContactsResponse,
    GetPhysicalLocationsResponse,
    GetShippingMethodsResponse,
)
from psdomain.model.base import ServiceMessage
from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty

if TYPE_CHECKING:
    from psdomain.proto.companydata import companydata_pb2 as proto


# --- Basic model converters ---

def address_to_proto(addr: Address, proto_module) -> 'proto.Address':
    return proto_module.Address(
        address_name=pydantic_str_or_empty(addr.address_name),
        attention_to=pydantic_str_or_empty(addr.attention_to),
        address1=pydantic_str_or_empty(addr.address1),
        address2=pydantic_str_or_empty(addr.address2),
        address3=pydantic_str_or_empty(addr.address3),
        city=pydantic_str_or_empty(addr.city),
        region=pydantic_str_or_empty(addr.region),
        postal_code=pydantic_str_or_empty(addr.postal_code),
        country=pydantic_str_or_empty(addr.country),
    )


def address_from_proto(p) -> Address:
    return Address(
        address_name=proto_str_or_none(p.address_name),
        attention_to=proto_str_or_none(p.attention_to),
        address1=proto_str_or_none(p.address1),
        address2=proto_str_or_none(p.address2),
        address3=proto_str_or_none(p.address3),
        city=proto_str_or_none(p.city),
        region=proto_str_or_none(p.region),
        postal_code=proto_str_or_none(p.postal_code),
        country=proto_str_or_none(p.country),
    )


def phone_to_proto(phone: Phone, proto_module) -> 'proto.Phone':
    return proto_module.Phone(
        phone_type=pydantic_str_or_empty(phone.phone_type),
        phone_number=pydantic_str_or_empty(phone.phone_number),
        phone_extension=pydantic_str_or_empty(phone.phone_extension),
    )


def phone_from_proto(p) -> Phone:
    return Phone(
        phone_type=proto_str_or_none(p.phone_type),
        phone_number=proto_str_or_none(p.phone_number),
        phone_extension=proto_str_or_none(p.phone_extension),
    )


def contact_to_proto(contact: Contact, proto_module) -> 'proto.Contact':
    result = proto_module.Contact(
        contact_name=pydantic_str_or_empty(contact.contact_name),
        contact_department=pydantic_str_or_empty(contact.contact_department),
        contact_role=pydantic_str_or_empty(contact.contact_role),
        contact_title=pydantic_str_or_empty(contact.contact_title),
        physical_location_id=pydantic_str_or_empty(contact.physical_location_id),
        business_line_id=pydantic_str_or_empty(contact.business_line_id),
        email=pydantic_str_or_empty(contact.email),
    )
    for phone in contact.phones:
        result.phones.append(phone_to_proto(phone, proto_module))
    return result


def contact_from_proto(p) -> Contact:
    return Contact(
        contact_name=proto_str_or_none(p.contact_name),
        contact_department=proto_str_or_none(p.contact_department),
        contact_role=proto_str_or_none(p.contact_role),
        contact_title=proto_str_or_none(p.contact_title),
        physical_location_id=proto_str_or_none(p.physical_location_id),
        business_line_id=proto_str_or_none(p.business_line_id),
        phones=[phone_from_proto(ph) for ph in p.phones],
        email=proto_str_or_none(p.email),
    )


def identifier_to_proto(ident: Identifier, proto_module) -> 'proto.Identifier':
    return proto_module.Identifier(
        identifier_type=pydantic_str_or_empty(ident.identifier_type),
        identifier_number=pydantic_str_or_empty(ident.identifier_number),
        country=pydantic_str_or_empty(ident.country),
        start_date=pydantic_str_or_empty(ident.start_date),
        expiry_date=pydantic_str_or_empty(ident.expiry_date),
    )


def identifier_from_proto(p) -> Identifier:
    return Identifier(
        identifier_type=proto_str_or_none(p.identifier_type),
        identifier_number=proto_str_or_none(p.identifier_number),
        country=proto_str_or_none(p.country),
        start_date=proto_str_or_none(p.start_date),
        expiry_date=proto_str_or_none(p.expiry_date),
    )


def brand_to_proto(brand: Brand, proto_module) -> 'proto.Brand':
    return proto_module.Brand(
        brand_id=pydantic_str_or_empty(brand.brand_id),
        brand_name=pydantic_str_or_empty(brand.brand_name),
        brand_logo_url=pydantic_str_or_empty(brand.brand_logo_url),
    )


def brand_from_proto(p) -> Brand:
    return Brand(
        brand_id=proto_str_or_none(p.brand_id),
        brand_name=proto_str_or_none(p.brand_name),
        brand_logo_url=proto_str_or_none(p.brand_logo_url),
    )


def business_line_to_proto(bl: BusinessLine, proto_module) -> 'proto.BusinessLine':
    result = proto_module.BusinessLine(
        business_line_id=pydantic_str_or_empty(bl.business_line_id),
        name=pydantic_str_or_empty(bl.name),
        website=pydantic_str_or_empty(bl.website),
        logo_url=pydantic_str_or_empty(bl.logo_url),
    )
    if bl.contact:
        result.contact.CopyFrom(contact_to_proto(bl.contact, proto_module))
    for ident in bl.identifiers:
        result.identifiers.append(identifier_to_proto(ident, proto_module))
    for brand in bl.brands:
        result.brands.append(brand_to_proto(brand, proto_module))
    return result


def business_line_from_proto(p) -> BusinessLine:
    contact = contact_from_proto(p.contact) if p.HasField('contact') else None
    return BusinessLine(
        business_line_id=proto_str_or_none(p.business_line_id),
        name=proto_str_or_none(p.name),
        website=proto_str_or_none(p.website),
        logo_url=proto_str_or_none(p.logo_url),
        contact=contact,
        identifiers=[identifier_from_proto(i) for i in p.identifiers],
        brands=[brand_from_proto(b) for b in p.brands],
    )


def company_data_to_proto(cd: CompanyData, proto_module) -> 'proto.CompanyData':
    result = proto_module.CompanyData(
        name=pydantic_str_or_empty(cd.name),
        website=pydantic_str_or_empty(cd.website),
        logo_url=pydantic_str_or_empty(cd.logo_url),
    )
    if cd.contact:
        result.contact.CopyFrom(contact_to_proto(cd.contact, proto_module))
    for ident in cd.identifiers:
        result.identifiers.append(identifier_to_proto(ident, proto_module))
    for bl in cd.business_lines:
        result.business_lines.append(business_line_to_proto(bl, proto_module))
    return result


def company_data_from_proto(p) -> CompanyData:
    contact = contact_from_proto(p.contact) if p.HasField('contact') else None
    return CompanyData(
        name=proto_str_or_none(p.name),
        website=proto_str_or_none(p.website),
        logo_url=proto_str_or_none(p.logo_url),
        contact=contact,
        identifiers=[identifier_from_proto(i) for i in p.identifiers],
        business_lines=[business_line_from_proto(bl) for bl in p.business_lines],
    )


# --- Other model converters ---

def business_characteristic_to_proto(bc: BusinessCharacteristic, proto_module):
    return proto_module.BusinessCharacteristic(
        business_characteristic_category=pydantic_str_or_empty(bc.business_characteristic_category),
        business_characteristic_name=pydantic_str_or_empty(bc.business_characteristic_name),
        business_characteristic_description=pydantic_str_or_empty(bc.business_characteristic_description),
    )


def business_characteristic_from_proto(p) -> BusinessCharacteristic:
    return BusinessCharacteristic(
        business_characteristic_category=proto_str_or_none(p.business_characteristic_category),
        business_characteristic_name=proto_str_or_none(p.business_characteristic_name),
        business_characteristic_description=proto_str_or_none(p.business_characteristic_description),
    )


def certification_to_proto(cert: Certification, proto_module):
    return proto_module.Certification(
        certification_category=pydantic_str_or_empty(cert.certification_category),
        certification_name=pydantic_str_or_empty(cert.certification_name),
        certification_number=pydantic_str_or_empty(cert.certification_number),
        start_date=pydantic_str_or_empty(cert.start_date),
        expiry_date=pydantic_str_or_empty(cert.expiry_date),
        certification_description=pydantic_str_or_empty(cert.certification_description),
        certification_url=pydantic_str_or_empty(cert.certification_url),
        certification_body_url=pydantic_str_or_empty(cert.certification_body_url),
    )


def certification_from_proto(p) -> Certification:
    return Certification(
        certification_category=proto_str_or_none(p.certification_category),
        certification_name=proto_str_or_none(p.certification_name),
        certification_number=proto_str_or_none(p.certification_number),
        start_date=proto_str_or_none(p.start_date),
        expiry_date=proto_str_or_none(p.expiry_date),
        certification_description=proto_str_or_none(p.certification_description),
        certification_url=proto_str_or_none(p.certification_url),
        certification_body_url=proto_str_or_none(p.certification_body_url),
    )


def payment_method_to_proto(pm: PaymentMethod, proto_module):
    return proto_module.PaymentMethod(
        payment_method_type=pydantic_str_or_empty(pm.payment_method_type),
        payment_method_name=pydantic_str_or_empty(pm.payment_method_name),
        payment_method_description=pydantic_str_or_empty(pm.payment_method_description),
        payment_method_surcharge=pm.payment_method_surcharge or 0.0,
    )


def payment_method_from_proto(p) -> PaymentMethod:
    return PaymentMethod(
        payment_method_type=proto_str_or_none(p.payment_method_type),
        payment_method_name=proto_str_or_none(p.payment_method_name),
        payment_method_description=proto_str_or_none(p.payment_method_description),
        payment_method_surcharge=p.payment_method_surcharge if p.payment_method_surcharge else None,
    )


def payment_terms_to_proto(pt: PaymentTerms, proto_module):
    return proto_module.PaymentTerms(
        payment_terms_name=pydantic_str_or_empty(pt.payment_terms_name),
        payment_terms_anchor=pydantic_str_or_empty(pt.payment_terms_anchor),
        payment_due_days=pt.payment_due_days or 0,
        payment_discount=pt.payment_discount or 0.0,
        payment_discount_days=pt.payment_discount_days or 0,
    )


def payment_terms_from_proto(p) -> PaymentTerms:
    return PaymentTerms(
        payment_terms_name=proto_str_or_none(p.payment_terms_name),
        payment_terms_anchor=proto_str_or_none(p.payment_terms_anchor),
        payment_due_days=p.payment_due_days if p.payment_due_days else None,
        payment_discount=p.payment_discount if p.payment_discount else None,
        payment_discount_days=p.payment_discount_days if p.payment_discount_days else None,
    )


def physical_location_to_proto(pl: PhysicalLocation, proto_module):
    result = proto_module.PhysicalLocation(
        physical_location_id=pydantic_str_or_empty(pl.physical_location_id),
        fob_id=pydantic_str_or_empty(pl.fob_id),
        inventory_location_id=pydantic_str_or_empty(pl.inventory_location_id),
        business_line_id=pydantic_str_or_empty(pl.business_line_id),
        default_shipping_method_id=pydantic_str_or_empty(pl.default_shipping_method_id),
    )
    if pl.address:
        result.address.CopyFrom(address_to_proto(pl.address, proto_module))
    return result


def physical_location_from_proto(p) -> PhysicalLocation:
    address = address_from_proto(p.address) if p.HasField('address') else None
    return PhysicalLocation(
        physical_location_id=proto_str_or_none(p.physical_location_id),
        address=address,
        fob_id=proto_str_or_none(p.fob_id),
        inventory_location_id=proto_str_or_none(p.inventory_location_id),
        business_line_id=proto_str_or_none(p.business_line_id),
        default_shipping_method_id=proto_str_or_none(p.default_shipping_method_id),
    )


def policy_to_proto(pol: Policy, proto_module):
    return proto_module.Policy(
        policy_category=pydantic_str_or_empty(pol.policy_category),
        policy_name=pydantic_str_or_empty(pol.policy_name),
        policy_description=pydantic_str_or_empty(pol.policy_description),
        start_date=pydantic_str_or_empty(pol.start_date),
        expiry_date=pydantic_str_or_empty(pol.expiry_date),
    )


def policy_from_proto(p) -> Policy:
    return Policy(
        policy_category=proto_str_or_none(p.policy_category),
        policy_name=proto_str_or_none(p.policy_name),
        policy_description=proto_str_or_none(p.policy_description),
        start_date=proto_str_or_none(p.start_date),
        expiry_date=proto_str_or_none(p.expiry_date),
    )


def promo_standards_service_to_proto(pss: PromoStandardsService, proto_module):
    return proto_module.PromoStandardsService(
        promo_standards_service_type=pydantic_str_or_empty(pss.promo_standards_service_type),
        ws_version=pydantic_str_or_empty(pss.ws_version),
    )


def promo_standards_service_from_proto(p) -> PromoStandardsService:
    return PromoStandardsService(
        promo_standards_service_type=proto_str_or_none(p.promo_standards_service_type),
        ws_version=proto_str_or_none(p.ws_version),
    )


def promo_standards_service_detail_to_proto(pssd: PromoStandardsServiceDetail, proto_module):
    return proto_module.PromoStandardsServiceDetail(
        promo_standards_service_type=pydantic_str_or_empty(pssd.promo_standards_service_type),
        ws_version=pydantic_str_or_empty(pssd.ws_version),
        endpoint_url=pydantic_str_or_empty(pssd.endpoint_url),
        wsdl_url=pydantic_str_or_empty(pssd.wsdl_url),
        environment=pydantic_str_or_empty(pssd.environment),
        country=pydantic_str_or_empty(pssd.country),
    )


def promo_standards_service_detail_from_proto(p) -> PromoStandardsServiceDetail:
    return PromoStandardsServiceDetail(
        promo_standards_service_type=proto_str_or_none(p.promo_standards_service_type),
        ws_version=proto_str_or_none(p.ws_version),
        endpoint_url=proto_str_or_none(p.endpoint_url),
        wsdl_url=proto_str_or_none(p.wsdl_url),
        environment=proto_str_or_none(p.environment),
        country=proto_str_or_none(p.country),
    )


def shipping_method_to_proto(sm: ShippingMethod, proto_module):
    result = proto_module.ShippingMethod(
        shipping_method_id=pydantic_str_or_empty(sm.shipping_method_id),
        shipping_method_name=pydantic_str_or_empty(sm.shipping_method_name),
        is_default_shipping_method=sm.is_default_shipping_method,
        shipping_method_carrier=pydantic_str_or_empty(sm.shipping_method_carrier),
        shipping_method_service=pydantic_str_or_empty(sm.shipping_method_service),
        shipping_account_type=pydantic_str_or_empty(sm.shipping_account_type),
    )
    result.physical_location_ids.extend(sm.physical_location_ids)
    return result


def shipping_method_from_proto(p) -> ShippingMethod:
    return ShippingMethod(
        shipping_method_id=proto_str_or_none(p.shipping_method_id),
        shipping_method_name=proto_str_or_none(p.shipping_method_name),
        is_default_shipping_method=p.is_default_shipping_method,
        shipping_method_carrier=proto_str_or_none(p.shipping_method_carrier),
        shipping_method_service=proto_str_or_none(p.shipping_method_service),
        shipping_account_type=proto_str_or_none(p.shipping_account_type),
        physical_location_ids=list(p.physical_location_ids),
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

def get_company_data_to_proto(response: GetCompanyDataResponse):
    """Convert pydantic GetCompanyDataResponse to proto."""
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetCompanyDataResponse()
    if response.company_data:
        result.company_data.CopyFrom(company_data_to_proto(response.company_data, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_company_data_from_proto(proto_msg) -> GetCompanyDataResponse:
    """Convert proto GetCompanyDataResponse to pydantic."""
    company_data = None
    if proto_msg.HasField('company_data'):
        company_data = company_data_from_proto(proto_msg.company_data)
    return GetCompanyDataResponse(
        company_data=company_data,
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


# Convenience aliases for main endpoint
to_proto = get_company_data_to_proto
from_proto = get_company_data_from_proto


# --- Additional response converters ---

def get_available_promo_standards_services_to_proto(response: GetAvailablePromoStandardsServicesResponse):
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetAvailablePromoStandardsServicesResponse()
    for pss in response.promo_standards_services:
        result.promo_standards_services.append(promo_standards_service_to_proto(pss, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_available_promo_standards_services_from_proto(proto_msg) -> GetAvailablePromoStandardsServicesResponse:
    return GetAvailablePromoStandardsServicesResponse(
        promo_standards_services=[promo_standards_service_from_proto(s) for s in proto_msg.promo_standards_services],
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


def get_certifications_to_proto(response: GetCertificationsResponse):
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetCertificationsResponse()
    for cert in response.certifications:
        result.certifications.append(certification_to_proto(cert, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_certifications_from_proto(proto_msg) -> GetCertificationsResponse:
    return GetCertificationsResponse(
        certifications=[certification_from_proto(c) for c in proto_msg.certifications],
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


def get_contacts_to_proto(response: GetContactsResponse):
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetContactsResponse()
    for contact in response.contacts:
        result.contacts.append(contact_to_proto(contact, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_contacts_from_proto(proto_msg) -> GetContactsResponse:
    return GetContactsResponse(
        contacts=[contact_from_proto(c) for c in proto_msg.contacts],
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


def get_physical_locations_to_proto(response: GetPhysicalLocationsResponse):
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetPhysicalLocationsResponse()
    for loc in response.physical_locations:
        result.physical_locations.append(physical_location_to_proto(loc, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_physical_locations_from_proto(proto_msg) -> GetPhysicalLocationsResponse:
    return GetPhysicalLocationsResponse(
        physical_locations=[physical_location_from_proto(pl) for pl in proto_msg.physical_locations],
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )


def get_shipping_methods_to_proto(response: GetShippingMethodsResponse):
    from psdomain.proto.companydata import companydata_pb2 as proto_module
    result = proto_module.GetShippingMethodsResponse()
    for sm in response.shipping_methods:
        result.shipping_methods.append(shipping_method_to_proto(sm, proto_module))
    for msg in response.service_messages:
        result.service_messages.append(service_message_to_proto(msg, proto_module))
    return result


def get_shipping_methods_from_proto(proto_msg) -> GetShippingMethodsResponse:
    return GetShippingMethodsResponse(
        shipping_methods=[shipping_method_from_proto(sm) for sm in proto_msg.shipping_methods],
        service_messages=[service_message_from_proto(m) for m in proto_msg.service_messages],
    )
