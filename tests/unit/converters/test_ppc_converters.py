"""
Tests for PPC v1.0.0 converters.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from decimal import Decimal

from psdomain.model.ppc import (
    AvailableLocationsResponse,
    AvailableLocationArray,
    DecorationColorResponse,
    DecorationColors,
    DecorationMethod,
    DecorationMethodArray,
    ColorArray,
    FobPointsResponse,
    FobPoint,
    FobPointArray,
    AvailableChargesResponse,
    AvailableCharge,
    AvailableChargeArray,
    ConfigurationAndPricingResponse,
    Configuration,
    Part,
    PartArray,
    PartPrice,
    PartPriceArray,
    Location,
    LocationArray,
    ChargeType,
)
from psdomain.model.product_data.common import Color, Location as ProductDataLocation
from psdomain.model.base import PriceType, UOM, Currency
from psdomain.converters.ppc import v100


class TestPPCAvailableLocationsConverter:
    """Tests for PPC Available Locations converter."""

    def test_basic_available_locations(self):
        """Test basic available locations response conversion."""
        location1 = ProductDataLocation(
            locationId=1,
            locationName="Front",
        )
        location2 = ProductDataLocation(
            locationId=2,
            locationName="Back",
        )

        response = AvailableLocationsResponse(
            AvailableLocationArray=AvailableLocationArray(AvailableLocation=[location1, location2]),
            ErrorMessage=None,
        )

        proto_response = v100.available_locations_to_proto(response)

        # Verify proto
        assert len(proto_response.locations) == 2
        assert proto_response.locations[0].location_id == 1
        assert proto_response.locations[0].location_name == "Front"

        # Roundtrip
        roundtrip = v100.available_locations_from_proto(proto_response)
        assert len(roundtrip.AvailableLocationArray.AvailableLocation) == 2
        assert roundtrip.AvailableLocationArray.AvailableLocation[0].locationName == "Front"


class TestPPCDecorationColorsConverter:
    """Tests for PPC Decoration Colors converter."""

    def test_decoration_colors_response(self):
        """Test decoration colors response conversion."""
        colors = ColorArray(Color=[
            Color(colorName="Red"),
            Color(colorName="Blue"),
        ])

        decoration_methods = DecorationMethodArray(DecorationMethod=[
            DecorationMethod(decorationId=1, decorationName="Screen Print"),
            DecorationMethod(decorationId=2, decorationName="Embroidery"),
        ])

        decoration_colors = DecorationColors(
            productId="PROD-001",
            locationId=1,
            pmsMatch=True,
            fullColor=False,
            ColorArray=colors,
            DecorationMethodArray=decoration_methods,
        )

        response = DecorationColorResponse(
            DecorationColors=decoration_colors,
            ErrorMessage=None,
        )

        proto_response = v100.decoration_colors_response_to_proto(response)

        # Verify proto
        assert proto_response.decoration_colors.product_id == "PROD-001"
        assert proto_response.decoration_colors.location_id == 1
        assert proto_response.decoration_colors.pms_match is True
        assert len(proto_response.decoration_colors.colors) == 2
        assert len(proto_response.decoration_colors.decoration_methods) == 2

        # Roundtrip
        roundtrip = v100.decoration_colors_response_from_proto(proto_response)
        assert roundtrip.DecorationColors.productId == "PROD-001"
        assert roundtrip.DecorationColors.pmsMatch is True


class TestPPCFobPointsConverter:
    """Tests for PPC FOB Points converter."""

    def test_fob_points_response(self):
        """Test FOB points response conversion."""
        fob_point = FobPoint(
            fobId="FOB-001",
            fobCity="Los Angeles",
            fobState="CA",
            fobPostalCode="90001",
            fobCountry="US",
            CurrencySupportedArray=None,
            ProductArray=None,
        )

        response = FobPointsResponse(
            FobPointArray=FobPointArray(FobPoint=[fob_point]),
            ErrorMessage=None,
        )

        proto_response = v100.fob_points_to_proto(response)

        # Verify proto
        assert len(proto_response.fob_points) == 1
        assert proto_response.fob_points[0].fob_id == "FOB-001"
        assert proto_response.fob_points[0].fob_city == "Los Angeles"
        assert proto_response.fob_points[0].fob_country == "US"

        # Roundtrip
        roundtrip = v100.fob_points_from_proto(proto_response)
        assert len(roundtrip.FobPointArray.FobPoint) == 1
        assert roundtrip.FobPointArray.FobPoint[0].fobCity == "Los Angeles"


class TestPPCAvailableChargesConverter:
    """Tests for PPC Available Charges converter."""

    def test_available_charges_response(self):
        """Test available charges response conversion."""
        charges = [
            AvailableCharge(
                chargeId=1,
                chargeName="Setup Charge",
                chargeType=ChargeType.SETUP,
                chargeDescription="Initial setup fee",
            ),
            AvailableCharge(
                chargeId=2,
                chargeName="Run Charge",
                chargeType=ChargeType.RUN,
                chargeDescription="Per item charge",
            ),
        ]

        response = AvailableChargesResponse(
            AvailableChargeArray=AvailableChargeArray(AvailableCharge=charges),
            ErrorMessage=None,
        )

        proto_response = v100.available_charges_to_proto(response)

        # Verify proto
        assert len(proto_response.charges) == 2
        assert proto_response.charges[0].charge_id == 1
        assert proto_response.charges[0].charge_name == "Setup Charge"
        assert proto_response.charges[0].charge_type == "Setup"

        # Roundtrip
        roundtrip = v100.available_charges_from_proto(proto_response)
        assert len(roundtrip.AvailableChargeArray.AvailableCharge) == 2
        assert roundtrip.AvailableChargeArray.AvailableCharge[0].chargeType == ChargeType.SETUP


class TestPPCConfigurationAndPricingConverter:
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

        proto_response = v100.config_and_pricing_to_proto(response)

        # Verify proto
        assert proto_response.configuration.product_id == "PROD-001"
        assert proto_response.configuration.currency == "USD"
        assert len(proto_response.configuration.parts) == 1
        assert proto_response.configuration.parts[0].part_id == "PART-001"

        # Roundtrip
        roundtrip = v100.config_and_pricing_from_proto(proto_response)
        assert roundtrip.Configuration.productId == "PROD-001"
        assert len(roundtrip.Configuration.parts) == 1

    def test_configuration_with_error(self):
        """Test configuration response with error message."""
        from psdomain.model.base import ErrorMessage

        response = ConfigurationAndPricingResponse(
            Configuration=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = v100.config_and_pricing_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404
        assert proto_response.error_message.description == "Product not found"

        # Roundtrip
        roundtrip = v100.config_and_pricing_from_proto(proto_response)
        assert roundtrip.Configuration is None
        assert roundtrip.ErrorMessage.code == 404
