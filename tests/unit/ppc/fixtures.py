import pytest

from psdomain.model import FobPointsResponse

from .responses.fob_points import json_response_ok


@pytest.fixture
def fob_points_ok() -> FobPointsResponse:
    yield FobPointsResponse.model_validate_json(json_response_ok)
