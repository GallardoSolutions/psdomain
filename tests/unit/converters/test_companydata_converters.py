"""
Tests for Company Data v1.0.0 converters.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.company_data import (
    Phone,
    Contact,
    Brand,
    BusinessLine,
    CompanyData,
    GetCompanyDataResponse,
)
from psdomain.model.base import ServiceMessage
from psdomain.converters.companydata import v100


class TestCompanyDataV100Converter:
    """Tests for Company Data v1.0.0 converter."""

    def test_basic_company_data_response(self):
        """Test basic company data response conversion."""
        company_data = CompanyData(
            name="Acme Corporation",
            website="https://acme.com",
            logo_url="https://acme.com/logo.png",
            contact=None,
            identifiers=[],
            business_lines=[],
        )

        response = GetCompanyDataResponse(
            company_data=company_data,
            service_messages=[],
        )

        proto_response = v100.get_company_data_to_proto(response)

        # Verify proto
        assert proto_response.company_data.name == "Acme Corporation"
        assert proto_response.company_data.website == "https://acme.com"

        # Roundtrip
        roundtrip = v100.get_company_data_from_proto(proto_response)
        assert roundtrip.company_data.name == "Acme Corporation"
        assert roundtrip.company_data.website == "https://acme.com"

    def test_company_data_with_contact(self):
        """Test company data with contact info."""
        phone = Phone(
            phone_type="Main",
            phone_number="555-1234",
            phone_extension="100",
        )

        contact = Contact(
            contact_name="Jane Doe",
            contact_department="Sales",
            contact_role="Manager",
            contact_title="Sales Manager",
            physical_location_id=None,
            business_line_id=None,
            phones=[phone],
            email="jane@acme.com",
        )

        company_data = CompanyData(
            name="Acme Corporation",
            website="https://acme.com",
            logo_url=None,
            contact=contact,
            identifiers=[],
            business_lines=[],
        )

        response = GetCompanyDataResponse(
            company_data=company_data,
            service_messages=[],
        )

        proto_response = v100.get_company_data_to_proto(response)

        # Verify contact in proto
        assert proto_response.company_data.contact.contact_name == "Jane Doe"
        assert proto_response.company_data.contact.email == "jane@acme.com"
        assert len(proto_response.company_data.contact.phones) == 1
        assert proto_response.company_data.contact.phones[0].phone_number == "555-1234"

        # Roundtrip
        roundtrip = v100.get_company_data_from_proto(proto_response)
        assert roundtrip.company_data.contact.contact_name == "Jane Doe"
        assert roundtrip.company_data.contact.phones[0].phone_number == "555-1234"

    def test_company_data_with_business_lines(self):
        """Test company data with business lines."""
        brand = Brand(
            brand_id="B001",
            brand_name="Premium Brand",
            brand_logo_url="https://acme.com/brand.png",
        )

        business_line = BusinessLine(
            business_line_id="BL001",
            name="Premium Products",
            website="https://premium.acme.com",
            logo_url=None,
            contact=None,
            identifiers=[],
            brands=[brand],
        )

        company_data = CompanyData(
            name="Acme Corporation",
            website=None,
            logo_url=None,
            contact=None,
            identifiers=[],
            business_lines=[business_line],
        )

        response = GetCompanyDataResponse(
            company_data=company_data,
            service_messages=[],
        )

        proto_response = v100.get_company_data_to_proto(response)

        # Verify business line in proto
        assert len(proto_response.company_data.business_lines) == 1
        assert proto_response.company_data.business_lines[0].name == "Premium Products"
        assert len(proto_response.company_data.business_lines[0].brands) == 1
        assert proto_response.company_data.business_lines[0].brands[0].brand_name == "Premium Brand"

        # Roundtrip
        roundtrip = v100.get_company_data_from_proto(proto_response)
        assert len(roundtrip.company_data.business_lines) == 1
        assert roundtrip.company_data.business_lines[0].name == "Premium Products"

    def test_company_data_with_service_messages(self):
        """Test company data response with service messages."""
        response = GetCompanyDataResponse(
            company_data=None,
            service_messages=[
                ServiceMessage(code=404, description="Company not found", severity="Error"),
            ],
        )

        proto_response = v100.get_company_data_to_proto(response)

        # Verify service messages
        assert len(proto_response.service_messages) == 1
        assert proto_response.service_messages[0].code == 404

        # Roundtrip
        roundtrip = v100.get_company_data_from_proto(proto_response)
        assert roundtrip.company_data is None
        assert len(roundtrip.service_messages) == 1
        assert roundtrip.service_messages[0].code == 404
