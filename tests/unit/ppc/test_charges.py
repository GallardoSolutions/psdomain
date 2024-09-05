# flake8: noqa F811
from psdomain.model.ppc import ChargeType, AvailableChargesResponse

from .fixtures import charges_ok  # noqa
from .responses.charges import json_charges_setup_in_caps


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


def test_json_charges_setup_in_caps():
    response = AvailableChargesResponse.model_validate(json_charges_setup_in_caps)
    assert response.ErrorMessage is None
    charges = response.charges
    assert len(charges) == 21
    charge = charges[1]
    assert charge.chargeId == 126578007
    assert charge.chargeName == 'Pad Print'
    assert charge.chargeDescription == 'Pad Print'
    assert charge.chargeType == ChargeType.SETUP
