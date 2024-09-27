# flake8: noqa F811
from psdomain.model.ppc import AvailableLocationsResponse

from .fixtures import locations_ok  # noqa

from .responses.locations import start_location_name_empty_response


def test_locations(locations_ok):
    resp = locations_ok
    loc = resp.locations[0]
    assert loc.locationId == 8
    assert loc.locationName == 'FRONT'
    assert resp.ErrorMessage is None


def test_start_location_name_empty():
    resp = AvailableLocationsResponse.model_validate(start_location_name_empty_response)
    loc = resp.locations[0]
    assert loc.locationId == 0
    assert loc.locationName is None
    assert resp.ErrorMessage.code == 204
    assert resp.ErrorMessage.description == '204: No Content Found'
