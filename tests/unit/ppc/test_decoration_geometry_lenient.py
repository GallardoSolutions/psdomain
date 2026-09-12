"""decorationGeometry values outside the PromoStandards enum must not reject the whole PPC response.

2026-09-12: LANCO answers "Box" for every decoration, so PSRESTful returned HTTP 400 for all LANCO
pricing calls. Unknown values map to OTHER; case/whitespace variants of known values still match.
"""
import copy

import pytest

from psdomain.model.ppc import ConfigurationAndPricingResponse, DecorationGeometryType
from tests.unit.ppc.responses.ppc import ppc_inch_instead_of_inches_response


def _response_with_geometry(value):
    data = copy.deepcopy(ppc_inch_instead_of_inches_response)
    decoration = data['Configuration']['LocationArray']['Location'][0]['DecorationArray']['Decoration'][0]
    decoration['decorationGeometry'] = value
    return data


@pytest.mark.parametrize('value, expected', [
    ('Box', DecorationGeometryType.OTHER),            # LANCO
    ('Oval', DecorationGeometryType.OTHER),
    ('rectangle', DecorationGeometryType.RECTANGLE),  # case-insensitive match
    (' Circle ', DecorationGeometryType.CIRCLE),
    ('N/A', DecorationGeometryType.NOT_AVAILABLE),    # existing synonym still works
    (None, DecorationGeometryType.OTHER),
])
def test_geometry_is_normalised_instead_of_rejected(value, expected):
    response = ConfigurationAndPricingResponse.model_validate(_response_with_geometry(value))
    assert response.is_ok
    assert response.locations[0].decorations[0].decorationGeometry == expected
