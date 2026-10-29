"""A decoration without a decorationName must not reject the whole PPC response.

2026-10-29: Ariel Premium answers an empty <decorationName/> for BIB-BL25, so PSRESTful returned
HTTP 400 ("decorationName: Input should be a valid string") for every pricing call on that product
and the normalized-pricing sweep stored it without charge prices. The spec makes the name
required, but a missing name is the supplier's problem with one decoration, not a reason to drop
the product's pricing: it becomes an empty string.
"""
import copy

import pytest

from psdomain.model.ppc import ConfigurationAndPricingResponse, Decoration, DecorationMethod
from tests.unit.ppc.responses.ppc import ppc_inch_instead_of_inches_response


def _response_with_decoration_name(value):
    data = copy.deepcopy(ppc_inch_instead_of_inches_response)
    decoration = data['Configuration']['LocationArray']['Location'][0]['DecorationArray']['Decoration'][0]
    decoration['decorationName'] = value
    return data


@pytest.mark.parametrize('value, expected', [
    (None, ''),                     # Ariel: empty <decorationName/>
    ('', ''),
    ('Screen Print', 'Screen Print'),  # real names pass through untouched
])
def test_decoration_name_is_tolerated_instead_of_rejected(value, expected):
    response = ConfigurationAndPricingResponse.model_validate(_response_with_decoration_name(value))
    assert response.is_ok
    assert response.locations[0].decorations[0].decorationName == expected


def test_decoration_model_accepts_missing_name():
    decoration = Decoration.model_validate({
        'decorationId': 1, 'decorationName': None, 'decorationGeometry': 'Rectangle',
        'decorationHeight': None, 'decorationWidth': None, 'decorationDiameter': None,
        'decorationUom': 'Inches', 'allowSubForDefaultLocation': None, 'allowSubForDefaultMethod': None,
        'ChargeArray': None, 'decorationUnitsIncluded': None, 'decorationUnitsIncludedUom': None,
        'decorationUnitsMax': None, 'defaultDecoration': None, 'leadTime': None, 'rushLeadTime': None,
    })
    assert decoration.decorationName == ''


@pytest.mark.parametrize('value, expected', [(None, ''), ('Laser Engrave', 'Laser Engrave')])
def test_decoration_method_accepts_missing_name(value, expected):
    # getDecorationColors lists methods with the same field; same tolerance.
    method = DecorationMethod.model_validate({'decorationId': 7, 'decorationName': value})
    assert method.decorationName == expected
