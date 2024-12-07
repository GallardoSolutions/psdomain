from datetime import datetime

from psdomain.model.osn.v_1_0_0 import Package


def test_shipping_account_can_be_none():
    data = {
        'id': 3,
        'trackingNumber': '282856555261',
        'shipmentDate': datetime.now(),
        'dimUOM': None,
        'length': None,
        'width': None,
        'height': None,
        'weightUOM': None,
        'weight': None,
        'carrier': 'FedEx',
        'shipmentMethod': 'FEDEX GROUND',
        'shipmentAccount': None,
        'shipmentTerms': None,
        'ItemArray': None
    }
    package = Package.model_validate(data)
    assert package.shippingAccount is None
