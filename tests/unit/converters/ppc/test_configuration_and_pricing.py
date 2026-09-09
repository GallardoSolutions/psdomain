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
    Charge,
    ChargeArray,
    ChargeType,
    Decoration,
    DecorationArray,
    DecorationGeometryType,
    DecorationUomType,
    LocationIdArray,
    LocationId,
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


# HIT returns ids above the signed 32-bit range (charge 2245162467 on product
# 85048). The PromoStandards XSD says xs:int, suppliers don't honour it, and
# with int32 proto fields the converter raised "Value out of range" and every
# protobuf response/cache write for the product was a 500 (PSRESTFUL-API-5).
BIG_ID = 2245162467


class TestIdsAboveInt32:

    @staticmethod
    def _response():
        charge = Charge(
            chargeId=BIG_ID, chargeName="Setup", chargeType=ChargeType.SETUP, chargeDescription="Setup fee",
            ChargePriceArray=None, chargesPerLocation=None, chargesPerColor=None,
        )
        decoration = Decoration(
            decorationId=BIG_ID + 1, decorationName="Screen Print", decorationGeometry=DecorationGeometryType.RECTANGLE,
            decorationHeight=None, decorationWidth=None, decorationDiameter=None,
            decorationUom=DecorationUomType.COLORS,
            allowSubForDefaultLocation=None, allowSubForDefaultMethod=None,
            ChargeArray=ChargeArray(Charge=[charge]),
            decorationUnitsIncluded=None, decorationUnitsIncludedUom=None, decorationUnitsMax=None,
            defaultDecoration=None, leadTime=None, rushLeadTime=None,
        )
        location = Location(
            locationId=BIG_ID + 2, locationName="Front",
            DecorationArray=DecorationArray(Decoration=[decoration]),
            decorationsIncluded=0, defaultLocation=True, maxDecoration=1, minDecoration=0, locationRank=None,
        )
        part = Part(
            partId="PART-001", partDescription=None,
            PartPriceArray=PartPriceArray(PartPrice=[]), partGroup=1, nextPartGroup=None,
            partGroupRequired=True, partGroupDescription="Main", ratio=Decimal("1"), defaultPart=True,
            LocationIdArray=LocationIdArray(LocationId=[LocationId(locationId=BIG_ID + 2)]),
        )
        config = Configuration(
            PartArray=PartArray(Part=[part]), LocationArray=LocationArray(Location=[location]),
            productId="85048", currency=Currency.USD, FobArray=None, fobPostalCode=None,
            priceType=PriceType.NET, configurationType=None,
        )
        return ConfigurationAndPricingResponse(Configuration=config, ErrorMessage=None)

    def test_charge_location_decoration_ids_survive_roundtrip(self):
        proto = configuration_and_pricing.config_and_pricing_to_proto(self._response())

        loc = proto.configuration.locations[0]
        assert loc.location_id == BIG_ID + 2
        assert loc.decorations[0].decoration_id == BIG_ID + 1
        assert loc.decorations[0].charges[0].charge_id == BIG_ID
        assert list(proto.configuration.parts[0].location_ids) == [BIG_ID + 2]

        # Wire round-trip (int64 varints) and back to pydantic.
        wire = proto.SerializeToString()
        back = configuration_and_pricing.config_and_pricing_from_proto(type(proto).FromString(wire))
        rt_loc = back.Configuration.LocationArray.Location[0]
        assert rt_loc.locationId == BIG_ID + 2
        assert rt_loc.DecorationArray.Decoration[0].decorationId == BIG_ID + 1
        assert rt_loc.DecorationArray.Decoration[0].ChargeArray.Charge[0].chargeId == BIG_ID
