"""
Tests for PPC FobPoints converter.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.ppc import (
    FobPointsResponse,
    FobPoint,
    FobPointArray,
    CurrencySupportedArray,
    CurrencySupported,
    Product,
    ProductArray,
)
from psdomain.model.base import Currency, ErrorMessage
from psdomain.converters.ppc import fob_points


class TestFobPointsConverter:
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

        proto_response = fob_points.fob_points_to_proto(response)

        # Verify proto
        assert len(proto_response.fob_points) == 1
        assert proto_response.fob_points[0].fob_id == "FOB-001"
        assert proto_response.fob_points[0].fob_city == "Los Angeles"
        assert proto_response.fob_points[0].fob_country == "US"

        # Roundtrip
        roundtrip = fob_points.fob_points_from_proto(proto_response)
        assert len(roundtrip.FobPointArray.FobPoint) == 1
        assert roundtrip.FobPointArray.FobPoint[0].fobCity == "Los Angeles"

    def test_fob_points_with_currencies_and_products(self):
        """Test FOB points with currencies and products."""
        fob_point = FobPoint(
            fobId="FOB-002",
            fobCity="New York",
            fobState="NY",
            fobPostalCode="10001",
            fobCountry="US",
            CurrencySupportedArray=CurrencySupportedArray(
                CurrencySupported=[
                    CurrencySupported(currency=Currency.USD),
                    CurrencySupported(currency=Currency.CAD),
                ]
            ),
            ProductArray=ProductArray(
                Product=[
                    Product(productId="PROD-001"),
                    Product(productId="PROD-002"),
                ]
            ),
        )

        response = FobPointsResponse(
            FobPointArray=FobPointArray(FobPoint=[fob_point]),
            ErrorMessage=None,
        )

        proto_response = fob_points.fob_points_to_proto(response)

        # Verify proto
        assert len(proto_response.fob_points[0].currencies_supported) == 2
        assert "USD" in proto_response.fob_points[0].currencies_supported
        assert len(proto_response.fob_points[0].product_ids) == 2

        # Roundtrip
        roundtrip = fob_points.fob_points_from_proto(proto_response)
        assert len(roundtrip.FobPointArray.FobPoint[0].CurrencySupportedArray.CurrencySupported) == 2

    def test_fob_points_with_error(self):
        """Test FOB points response with error message."""
        response = FobPointsResponse(
            FobPointArray=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = fob_points.fob_points_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404
        assert proto_response.error_message.description == "Product not found"

        # Roundtrip
        roundtrip = fob_points.fob_points_from_proto(proto_response)
        assert roundtrip.FobPointArray is None
        assert roundtrip.ErrorMessage.code == 404
