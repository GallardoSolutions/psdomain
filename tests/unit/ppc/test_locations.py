# flake8: noqa F811
from .fixtures import locations_ok  # noqa


def test_locations(locations_ok):
    resp = locations_ok
    loc = resp.locations[0]
    assert loc.locationId == 8
    assert loc.locationName == 'FRONT'
    assert resp.ErrorMessage is None
