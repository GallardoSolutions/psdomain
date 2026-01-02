"""
Tests for PPC ConfigurationAndPricing converter.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from decimal import Decimal

from psdomain.model.ppc import (
    ConfigurationAndPricingResponse,
    Configuration,
    Part,
    PartArray,
    PartPrice,
    PartPriceArray,
    Location,
    LocationArray,
)
from psdomain.model.base import PriceType, UOM, Currency, ErrorMessage
from psdomain.converters.ppc import configuration_and_pricing


class TestConfigurationAndPricingConverter:
    """Tests for PPC Configuration and Pricing converter."""

    def test_configuration_and_pricing(self):
        """Test configuration and pricing response conversion."""
        part_price = PartPrice(
            minQuantity=1,
            price=Decimal("10.00"),
            discountCode="A",
            priceUom=UOM.EA,
            priceEffectiveDate=None,
            priceExpiryDate=None,
        )

        part = Part(
            partId="PART-001",
            partDescription="Test Part",
            PartPriceArray=PartPriceArray(PartPrice=[part_price]),
            partGroup=1,
            nextPartGroup=None,
            partGroupRequired=True,
            partGroupDescription="Main Product",
            ratio=Decimal("1"),
            defaultPart=True,
            LocationIdArray=None,
        )

        location = Location(
            locationId=1,
            locationName="Front",
            DecorationArray=None,
            maxDecoration=1,
            minDecoration=0,
            locationRank=1,
            decorationsIncluded=0,
            defaultLocation=True,
        )

        config = Configuration(
            PartArray=PartArray(Part=[part]),
            LocationArray=LocationArray(Location=[location]),
            productId="PROD-001",
            currency=Currency.USD,
            FobArray=None,
            fobPostalCode=None,
            priceType=PriceType.LIST,
            configurationType=None,
        )

        response = ConfigurationAndPricingResponse(
            Configuration=config,
            ErrorMessage=None,
        )

        proto_response = configuration_and_pricing.config_and_pricing_to_proto(response)

        # Verify proto
        assert proto_response.configuration.product_id == "PROD-001"
        assert proto_response.configuration.currency == "USD"
        assert len(proto_response.configuration.parts) == 1
        assert proto_response.configuration.parts[0].part_id == "PART-001"

        # Roundtrip
        roundtrip = configuration_and_pricing.config_and_pricing_from_proto(proto_response)
        assert roundtrip.Configuration.productId == "PROD-001"
        assert len(roundtrip.Configuration.parts) == 1

    def test_configuration_with_error(self):
        """Test configuration response with error message."""
        response = ConfigurationAndPricingResponse(
            Configuration=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = configuration_and_pricing.config_and_pricing_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404
        assert proto_response.error_message.description == "Product not found"

        # Roundtrip
        roundtrip = configuration_and_pricing.config_and_pricing_from_proto(proto_response)
        assert roundtrip.Configuration is None
        assert roundtrip.ErrorMessage.code == 404

    def test_configuration_with_multiple_parts(self):
        """Test configuration with multiple parts and prices."""
        part_price1 = PartPrice(
            minQuantity=1,
            price=Decimal("15.00"),
            discountCode="A",
            priceUom=UOM.EA,
            priceEffectiveDate=None,
            priceExpiryDate=None,
        )
        part_price2 = PartPrice(
            minQuantity=100,
            price=Decimal("12.00"),
            discountCode="B",
            priceUom=UOM.EA,
            priceEffectiveDate=None,
            priceExpiryDate=None,
        )

        part1 = Part(
            partId="PART-001",
            partDescription="Small Widget",
            PartPriceArray=PartPriceArray(PartPrice=[part_price1, part_price2]),
            partGroup=1,
            nextPartGroup=None,
            partGroupRequired=True,
            partGroupDescription="Widgets",
            ratio=Decimal("1"),
            defaultPart=True,
            LocationIdArray=None,
        )
        part2 = Part(
            partId="PART-002",
            partDescription="Large Widget",
            PartPriceArray=PartPriceArray(PartPrice=[part_price1]),
            partGroup=1,
            nextPartGroup=None,
            partGroupRequired=True,
            partGroupDescription="Widgets",
            ratio=Decimal("1"),
            defaultPart=False,
            LocationIdArray=None,
        )

        config = Configuration(
            PartArray=PartArray(Part=[part1, part2]),
            LocationArray=None,
            productId="PROD-002",
            currency=Currency.CAD,
            FobArray=None,
            fobPostalCode=None,
            priceType=PriceType.NET,
            configurationType=None,
        )

        response = ConfigurationAndPricingResponse(
            Configuration=config,
            ErrorMessage=None,
        )

        proto_response = configuration_and_pricing.config_and_pricing_to_proto(response)

        # Verify proto
        assert proto_response.configuration.product_id == "PROD-002"
        assert proto_response.configuration.currency == "CAD"
        assert len(proto_response.configuration.parts) == 2
        assert len(proto_response.configuration.parts[0].part_prices) == 2
        assert len(proto_response.configuration.parts[1].part_prices) == 1

        # Roundtrip
        roundtrip = configuration_and_pricing.config_and_pricing_from_proto(proto_response)
        assert len(roundtrip.Configuration.parts) == 2
        assert roundtrip.Configuration.currency == Currency.CAD
