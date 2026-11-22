"""Product Data 1.0.0 and the "latest" model used to type LocationDecorationArray, ProductPriceGroupArray and
FobPointArray as NoneType (the field's own default shadowed its class), so a product that carried any of them
was rejected. They now validate into their real models."""
import copy

import pytest

from psdomain.model.product_data.common import FobPointArray, LocationDecorationArray, ProductPriceGroupArray
from psdomain.model.product_data.latest import ProductResponseLatest
from psdomain.model.product_data.v_1_0_0 import ProductResponseV100

from .responses.products import resp01940E1

ARRAYS = {
    'LocationDecorationArray': {'LocationDecoration': [
        {'locationName': 'Front', 'maxImprintColors': 4, 'decorationName': 'Screen Print',
         'locationDecorationComboDefault': True, 'priceIncludes': False},
    ]},
    'ProductPriceGroupArray': {'ProductPriceGroup': [
        {'groupName': 'Standard', 'currency': 'USD', 'description': None, 'ProductPriceArray': None},
    ]},
    'FobPointArray': {'FobPoint': [
        {'fobId': '1', 'fobPostalCode': '27609', 'fobCity': 'Raleigh', 'fobState': 'NC', 'fobCountry': 'US'},
    ]},
}


def _base_response():
    resp = copy.deepcopy(resp01940E1)
    resp.setdefault('ErrorMessage', None)  # the 1.0.0 response requires the key; the 2.0.0 fixture omits it
    return resp


def _response_with_arrays():
    resp = _base_response()
    resp['Product'].update(copy.deepcopy(ARRAYS))
    return resp


@pytest.mark.parametrize('response_cls', [ProductResponseV100, ProductResponseLatest])
def test_product_arrays_validate_into_their_models(response_cls):
    product = response_cls.model_validate(_response_with_arrays()).Product

    assert isinstance(product.LocationDecorationArray, LocationDecorationArray)
    assert product.LocationDecorationArray.LocationDecoration[0].decorationName == 'Screen Print'
    assert isinstance(product.ProductPriceGroupArray, ProductPriceGroupArray)
    assert product.ProductPriceGroupArray.ProductPriceGroup[0].currency == 'USD'
    assert isinstance(product.FobPointArray, FobPointArray)
    assert product.FobPointArray.FobPoint[0].fobPostalCode == '27609'


@pytest.mark.parametrize('response_cls', [ProductResponseV100, ProductResponseLatest])
def test_product_arrays_dump_back_unchanged(response_cls):
    dumped = response_cls.model_validate(_response_with_arrays()).model_dump(mode='json')['Product']

    for name, value in ARRAYS.items():
        assert dumped[name] == value


@pytest.mark.parametrize('response_cls', [ProductResponseV100, ProductResponseLatest])
def test_product_without_the_arrays_still_defaults_them_to_none(response_cls):
    resp = _base_response()
    for name in ARRAYS:
        resp['Product'].pop(name, None)

    product = response_cls.model_validate(resp).Product

    arrays = (product.LocationDecorationArray, product.ProductPriceGroupArray, product.FobPointArray)
    assert arrays == (None, None, None)


def test_v100_fob_points_stays_empty_even_with_a_fob_point_array():
    """ProductV100.fob_points deliberately ignores FOB data (1.0.0 has none); accepting the array changes nothing."""
    product = ProductResponseV100.model_validate(_response_with_arrays()).Product

    assert product.fob_points == []
