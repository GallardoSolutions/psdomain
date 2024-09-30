# flake8: noqa F811
from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from .fixtures import ppc_blank_ok, ppc_decorated_ok  # noqa
from .responses.ppc import json_ppc_empty_response, ppc_inch_instead_of_inches_response, \
    ppc_decoration_arr_non_existing, ppc_unknown_price_uom_response, ppc_square_inches_response

from psdomain.model.ppc import DecorationGeometryType, DecorationUomType, ConfigurationAndPricingResponse


def test_is_ok(ppc_blank_ok):
    assert ppc_blank_ok.ErrorMessage is None
    assert ppc_blank_ok.is_ok


def test_parts(ppc_decorated_ok):
    parts = ppc_decorated_ok.parts
    assert len(parts) == 1
    part = parts[0]
    assert part.partId == '1035ATHGLD'
    assert part.partDescription == 'ATHLETIC GOLD'
    assert part.partGroup == 1
    assert part.nextPartGroup is None
    assert part.partGroupRequired
    assert part.partGroupDescription == 'Part Group'
    assert part.ratio == 1.0
    assert part.defaultPart is None
    locs = part.location_ids
    assert len(locs) == 1
    assert locs[0] == 8


def test_part_get_price(ppc_decorated_ok):
    part = ppc_decorated_ok.parts[0]
    price = part.get_price(144)
    assert price.price == Decimal('2.6940')
    assert price.minQuantity == 144
    assert price.discountCode is None
    assert price.priceUom == 'EA'
    assert price.priceEffectiveDate == datetime(2024, 2, 21, 0, 0)
    assert price.priceExpiryDate == datetime(2025, 2, 22, 0, 0)


def test_locations(ppc_blank_ok, ppc_decorated_ok):
    locations = ppc_blank_ok.locations
    # blank response has no locations
    assert len(locations) == 0
    #
    locations = ppc_decorated_ok.locations
    assert len(locations) == 1
    loc = locations[0]
    assert loc.locationId == 8
    assert loc.locationName == 'FRONT'
    assert loc.decorationsIncluded == 1
    assert loc.defaultLocation
    assert loc.maxDecoration == 1
    assert loc.minDecoration == 0
    assert loc.locationRank == 1
    decorations = loc.decorations
    assert len(decorations) == 3


def test_decorations(ppc_decorated_ok):
    locations = ppc_decorated_ok.locations
    loc = locations[0]
    decorations = loc.decorations
    decoration = decorations[0]
    assert decoration.decorationId == 1265947
    assert decoration.decorationName == 'TRANSFER'
    assert decoration.decorationGeometry == DecorationGeometryType.RECTANGLE
    assert decoration.decorationHeight == 1.875
    assert decoration.decorationWidth == 4.0
    assert decoration.decorationDiameter is None
    assert decoration.decorationUom == DecorationUomType.INCHES
    assert not decoration.allowSubForDefaultLocation
    assert not decoration.allowSubForDefaultMethod
    assert decoration.itemPartQuantityLTM == 50


def test_decoration_charges(ppc_decorated_ok):
    decoration = ppc_decorated_ok.locations[0].decorations[0]
    charges = decoration.charges
    assert len(charges) == 3
    charge = charges[0]
    assert charge.chargeId == 4389275
    assert charge.chargeName == 'TRANSFER'
    assert charge.chargeType == 'Setup'
    assert charge.chargeDescription == 'TRANSFER'
    assert charge.chargesAppliesLTM is None
    assert charge.chargesPerLocation is None
    assert charge.chargesPerColor is None


def test_charge_prices(ppc_decorated_ok):
    decoration = ppc_decorated_ok.locations[0].decorations[0]
    charge_prices = decoration.charges[0].prices
    assert len(charge_prices) == 1
    charge_price = charge_prices[0]
    assert charge_price.xMinQty == 1
    assert charge_price.xUom == 'EA'
    assert charge_price.yMinQty == 1
    assert charge_price.yUom == 'Colors'
    assert charge_price.price == 40.0
    assert charge_price.discountCode is None
    assert charge_price.repeatPrice == 20.0
    assert charge_price.repeatDiscountCode is None
    assert charge_price.priceEffectiveDate == datetime(2020, 2, 26, 0, 0)
    assert charge_price.priceExpiryDate == datetime(2028, 1, 1, 0, 0)


def test_empty_response():
    response = ConfigurationAndPricingResponse.model_validate_json(json_ppc_empty_response)
    assert response.ErrorMessage is None
    assert response.is_ok
    assert len(response.parts) == 0
    assert len(response.locations) == 0


def test_inch_instead_of_inches():
    response = ConfigurationAndPricingResponse.model_validate(ppc_inch_instead_of_inches_response)
    assert response.ErrorMessage is None
    assert response.is_ok
    decoration = response.locations[0].decorations[0]
    assert decoration.decorationHeight is None
    assert decoration.decorationWidth is None
    assert decoration.decorationDiameter is None
    assert decoration.decorationUom == DecorationUomType.INCHES


def test_ppc_decoration_arr_non_existing():
    response = ConfigurationAndPricingResponse.model_validate(ppc_decoration_arr_non_existing)
    assert response.ErrorMessage is None
    assert response.is_ok
    loc = response.locations[0]
    assert loc.decorations == []


def test_ppc_unknown_price_uom_response():
    # priceUom = "C" is not a valid value
    with pytest.raises(ValidationError):
        ConfigurationAndPricingResponse.model_validate(ppc_unknown_price_uom_response)


def test_square_inches_decoration():
    response = ConfigurationAndPricingResponse.model_validate_json(ppc_square_inches_response)
    assert response.ErrorMessage is None
    assert response.is_ok
    decoration = response.locations[0].decorations[1]
    assert decoration.decorationUnitsIncludedUom == DecorationUomType.SQUARE_INCHES


def test_min_part_qty():
    # because parts is empty, min_part_qty should return None
    response = ConfigurationAndPricingResponse.model_validate_json(json_ppc_empty_response)
    assert response.min_part_qty is None
    #
    resp = ConfigurationAndPricingResponse.model_validate(ppc_decoration_arr_non_existing)
    assert resp.min_part_qty == 50


def test_first_rush_lead_time(ppc_decorated_ok):
    response = ConfigurationAndPricingResponse.model_validate_json(json_ppc_empty_response)
    assert response.first_rush_lead_time is None
    #
    resp = ConfigurationAndPricingResponse.model_validate(ppc_decoration_arr_non_existing)
    assert resp.first_rush_lead_time is None
    #
    assert ppc_decorated_ok.first_rush_lead_time == 1


def test_ltm_qty(ppc_decorated_ok):
    assert ppc_decorated_ok.ltm_qty == 50
