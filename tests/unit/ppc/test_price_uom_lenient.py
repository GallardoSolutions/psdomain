"""A part price with a non-standard priceUom must not reject the whole PPC response.

HIT answers priceUom "C" (its discount-code letter) for every price of its stylus pens (17286,
17312), and an empty <priceUom/> for the main colour parts of others (5790COFF). PSRESTful returned
HTTP 400 ("priceUom: Input should be 'BX', 'CA', ...") for every pricing call on those products, so
CSV exports failed (PSRESTFUL-DJANGO-100, 51 events in October 2026) and the normalized-pricing
sweep skipped them. The spec restricts the unit to the UOM enum, but a wrong code on the
supplier's side is not a reason to drop a product's pricing: anything the enum does not know
becomes EA, the unit every one of those prices actually is.
"""
import copy

import pytest

from psdomain.model.base import UOM
from psdomain.model.ppc import ConfigurationAndPricingResponse, PartPrice
from tests.unit.ppc.responses.ppc import ppc_unknown_price_uom_response


def _part_price(value):
    return PartPrice.model_validate({
        'minQuantity': 200, 'discountCode': 'C', 'price': '2.42', 'priceUom': value,
        'priceEffectiveDate': None, 'priceExpiryDate': None,
    })


@pytest.mark.parametrize('value, expected', [
    ('C', UOM.EA),       # HIT 17286/17312: discount-code letter in the unit field
    (None, UOM.EA),      # HIT 5790COFF: empty <priceUom/>; also what the protobuf decoder yields
    ('', UOM.EA),
    ('ea', UOM.EA),      # case slips are still the real unit
    ('dz', UOM.DZ),
    ('DZ', UOM.DZ),      # valid units pass through untouched
    ('TH', UOM.TH),
    (UOM.PR, UOM.PR),
])
def test_price_uom_is_tolerated_instead_of_rejected(value, expected):
    assert _part_price(value).priceUom == expected


def test_hit_response_with_unknown_price_uom_validates():
    response = ConfigurationAndPricingResponse.model_validate(copy.deepcopy(ppc_unknown_price_uom_response))
    assert response.is_ok
    prices = [price for part in response.parts for price in part.prices]
    assert prices, 'the fixture carries HIT part prices'
    assert {price.priceUom for price in prices} == {UOM.EA}


def test_price_uom_round_trips_through_json():
    # The REST payload keeps serving the enum value, never the supplier's raw code.
    assert _part_price('C').model_dump(mode='json')['priceUom'] == 'EA'


def test_price_uom_survives_the_protobuf_wire():
    # The gateway and the Django client move prices as protobuf, where an empty unit arrives as an
    # absent field and used to decode to None; the decoded response must validate like the JSON one.
    from psdomain.converters.ppc import configuration_and_pricing as cppc
    response = ConfigurationAndPricingResponse.model_validate(copy.deepcopy(ppc_unknown_price_uom_response))
    proto = cppc.config_and_pricing_to_proto(response)
    for part in proto.configuration.parts:
        for price in part.part_prices:
            price.ClearField('price_uom')  # what a gateway relaying HIT's empty element produces
    back = cppc.config_and_pricing_from_proto(type(proto).FromString(proto.SerializeToString()))
    assert {price.priceUom for part in back.parts for price in part.prices} == {UOM.EA}
