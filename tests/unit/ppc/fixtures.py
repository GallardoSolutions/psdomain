import pytest

from psdomain.model import FobPointsResponse, AvailableLocationsResponse, AvailableChargesResponse, \
    DecorationColorResponse, ConfigurationAndPricingResponse

from .responses.fob_points import json_response_ok
from .responses.locations import json_locations_response_ok
from .responses.charges import json_charges_ok
from .responses.decoration_colors import json_decoration_colors_response_ok
from .responses.ppc import json_ppc_blank_response_ok, json_ppc_decorated_response_ok


@pytest.fixture
def fob_points_ok() -> FobPointsResponse:
    yield FobPointsResponse.model_validate_json(json_response_ok)


@pytest.fixture
def locations_ok() -> AvailableLocationsResponse:
    yield AvailableLocationsResponse.model_validate_json(json_locations_response_ok)


@pytest.fixture
def charges_ok() -> AvailableChargesResponse:
    yield AvailableChargesResponse.model_validate_json(json_charges_ok)


@pytest.fixture
def decoration_colors_ok() -> DecorationColorResponse:
    yield DecorationColorResponse.model_validate_json(json_decoration_colors_response_ok)


@pytest.fixture
def ppc_blank_ok() -> ConfigurationAndPricingResponse:
    yield ConfigurationAndPricingResponse.model_validate_json(json_ppc_blank_response_ok)


@pytest.fixture
def ppc_decorated_ok() -> ConfigurationAndPricingResponse:
    yield ConfigurationAndPricingResponse.model_validate_json(json_ppc_decorated_response_ok)
