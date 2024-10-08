# flake8: noqa F811
from .fixtures import fob_points_ok  # noqa
from .responses.fob_points import snugz_fob_point_china_response, snugs_fob_point_united_states_response, \
    pcna_fob_point_usa_response

from psdomain.model.ppc import FobPointsResponse
from psdomain.model.base import Currency


def test_get_fob_points(fob_points_ok):
    resp = fob_points_ok
    fp = resp.fob_points[0]
    assert fp.fobId == '1'
    assert fp.fobPostalCode == '33777'
    assert fp.fobCity == 'Largo'
    assert fp.fobState == 'FL'
    assert fp.fobCountry == 'US'
    #
    assert fp.CurrencySupportedArray.CurrencySupported[0].currency == 'USD'
    assert fp.CurrencySupportedArray.CurrencySupported[1].currency == 'CAD'
    assert fp.ProductArray.Product[0].productId == '1035'
    assert fp.ProductArray.Product[1].productId == '2799'
    assert fp.ProductArray.Product[2].productId == '20102'
    assert resp.ErrorMessage is None


def test_fob_points_id(fob_points_ok):
    lst = fob_points_ok.fob_point_ids
    assert lst == ['1']


def test_currencies_in_fp(fob_points_ok):
    fp = fob_points_ok.fob_points[0]
    lst = fp.currencies
    assert lst == ['USD', 'CAD']


def test_currencies_in_response(fob_points_ok):
    got = fob_points_ok.currencies
    assert got == {'USD', 'CAD'}


def test_snugz_china():
    resp = FobPointsResponse.model_validate(snugz_fob_point_china_response)
    fp = resp.fob_points[0]
    assert fp.fobId == '5'
    assert fp.fobPostalCode == 'Direct'
    assert fp.fobCity is None
    assert fp.fobState == 'China'
    assert fp.fobCountry == 'CN'


def test_snugz_united_states():
    resp = FobPointsResponse.model_validate(snugs_fob_point_united_states_response)
    fp = resp.fob_points[0]
    assert fp.fobId == '23'
    assert fp.fobPostalCode == '79906'
    assert fp.fobCity == 'El Paso'
    assert fp.fobState == 'TX'
    assert fp.fobCountry == 'US'


def test_pcna_usa():
    resp = FobPointsResponse.model_validate(pcna_fob_point_usa_response)
    fp = resp.fob_points[0]
    assert fp.fobId == '15068'
    assert fp.fobPostalCode == '15068'
    assert fp.fobCity == 'New Kensington'
    assert fp.fobState == 'PA'
    assert fp.fobCountry == 'US'
    assert fp.currencies == [Currency.CAD, Currency.USD]
