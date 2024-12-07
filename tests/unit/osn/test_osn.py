from datetime import datetime

from psdomain.model.osn.v_1_0_0 import ShipmentLocation


def test_shipping_location():
    now = datetime.now()
    data = {
        'id': 1,
        'complete': True,
        'ShipFromAddress': {
            'address1': '7055 Northwinds Drive NW',
            'address2': None,
            'address3': None,
            'address4': None,
            'city': 'Concord',
            'region': 'NC',
            'postalCode': '28027',
            'country': None
        },
        'ShipToAddress': {
            'address1': None,
            'address2': 'Suite B',
            'address3': None,
            'address4': None,
            'city': 'Piscataway',
            'region': 'NJ',
            'postalCode': '08854',
            'country': None
        },
        'shipmentDestinationType': None,
        'PackageArray': {
            'Package': [
                {
                    'id': 1,
                    'trackingNumber': '282856554004',
                    'shipmentDate': now,
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

            ]
        }
    }
    shipment_location = ShipmentLocation.model_validate(data)
    assert shipment_location.ShipFromAddress.city == 'Concord'
    assert shipment_location.ShipToAddress.city == 'Piscataway'
    assert shipment_location.ShipToAddress.address1 is None
