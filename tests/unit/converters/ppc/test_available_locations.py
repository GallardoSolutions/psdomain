"""
Tests for PPC AvailableLocations converter.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.ppc import (
    AvailableLocationsResponse,
    AvailableLocationArray,
)
from psdomain.model.product_data.common import Location as ProductDataLocation
from psdomain.model.base import ErrorMessage
from psdomain.converters.ppc import available_locations


class TestAvailableLocationsConverter:
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

        proto_response = available_locations.available_locations_to_proto(response)

        # Verify proto
        assert len(proto_response.locations) == 2
        assert proto_response.locations[0].location_id == 1
        assert proto_response.locations[0].location_name == "Front"

        # Roundtrip
        roundtrip = available_locations.available_locations_from_proto(proto_response)
        assert len(roundtrip.AvailableLocationArray.AvailableLocation) == 2
        assert roundtrip.AvailableLocationArray.AvailableLocation[0].locationName == "Front"

    def test_empty_available_locations(self):
        """Test empty available locations response."""
        response = AvailableLocationsResponse(
            AvailableLocationArray=None,
            ErrorMessage=None,
        )

        proto_response = available_locations.available_locations_to_proto(response)

        # Verify proto
        assert len(proto_response.locations) == 0

        # Roundtrip
        roundtrip = available_locations.available_locations_from_proto(proto_response)
        assert roundtrip.AvailableLocationArray is None

    def test_available_locations_with_error(self):
        """Test available locations response with error message."""
        response = AvailableLocationsResponse(
            AvailableLocationArray=None,
            ErrorMessage=ErrorMessage(code=404, description="Product not found"),
        )

        proto_response = available_locations.available_locations_to_proto(response)

        # Verify error
        assert proto_response.error_message.code == 404

        # Roundtrip
        roundtrip = available_locations.available_locations_from_proto(proto_response)
        assert roundtrip.AvailableLocationArray is None
        assert roundtrip.ErrorMessage.code == 404
