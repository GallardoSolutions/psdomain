"""
Tests for PPC DecorationColors converter.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.ppc import (
    DecorationColorResponse,
    DecorationColors,
    DecorationMethod,
    DecorationMethodArray,
    ColorArray,
)
from psdomain.model.product_data.common import Color
from psdomain.model.base import ErrorMessage
from psdomain.converters.ppc import decoration_colors


class TestDecorationColorsConverter:
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

        decoration_colors_data = DecorationColors(
            productId="PROD-001",
            locationId=1,
            pmsMatch=True,
            fullColor=False,
            ColorArray=colors,
            DecorationMethodArray=decoration_methods,
        )

        response = DecorationColorResponse(
            DecorationColors=decoration_colors_data,
            ErrorMessage=None,
        )

        proto_response = decoration_colors.decoration_colors_response_to_proto(response)

        # Verify proto
        assert proto_response.decoration_colors.product_id == "PROD-001"
        assert proto_response.decoration_colors.location_id == 1
        assert proto_response.decoration_colors.pms_match is True
        assert len(proto_response.decoration_colors.colors) == 2
        assert len(proto_response.decoration_colors.decoration_methods) == 2

        # Roundtrip
        roundtrip = decoration_colors.decoration_colors_response_from_proto(proto_response)
        assert roundtrip.DecorationColors.productId == "PROD-001"
        assert roundtrip.DecorationColors.pmsMatch is True

    def test_decoration_colors_minimal(self):
        """Test decoration colors with minimal data."""
        decoration_colors_data = DecorationColors(
            productId="PROD-002",
            locationId=2,
            pmsMatch=None,
            fullColor=None,
            ColorArray=None,
            DecorationMethodArray=None,
        )

        response = DecorationColorResponse(
            DecorationColors=decoration_colors_data,
            ErrorMessage=None,
        )

        proto_response = decoration_colors.decoration_colors_response_to_proto(response)

        # Verify proto
        assert proto_response.decoration_colors.product_id == "PROD-002"
        assert len(proto_response.decoration_colors.colors) == 0

        # Roundtrip
        roundtrip = decoration_colors.decoration_colors_response_from_proto(proto_response)
        assert roundtrip.DecorationColors.productId == "PROD-002"

    def test_decoration_colors_with_error(self):
        """Test decoration colors response with error message."""
        response = DecorationColorResponse(
            DecorationColors=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = decoration_colors.decoration_colors_response_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404

        # Roundtrip
        roundtrip = decoration_colors.decoration_colors_response_from_proto(proto_response)
        assert roundtrip.DecorationColors is None
        assert roundtrip.ErrorMessage.code == 404
