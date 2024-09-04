# flake8: noqa F811
from .fixtures import fob_points_ok  # noqa


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

