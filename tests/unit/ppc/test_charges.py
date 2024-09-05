# flake8: noqa F811
from psdomain.model.ppc import ChargeType

from .fixtures import charges_ok  # noqa


def test_charges(charges_ok):
    resp = charges_ok
    assert resp.ErrorMessage is None
    charges = resp.charges
    assert len(charges) == 9
    charge = charges[0]
    assert charge.chargeId == 4389275
    assert charge.chargeName == 'Transfer'
    assert charge.chargeType == ChargeType.SETUP
    assert charge.chargeDescription == 'Transfer'
