from datetime import datetime
from decimal import Decimal

from psdomain.model.osn.v_1_0_0 import ShipmentLocation, GetOrderShipmentNotificationResponse, Address


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
            'city': 'Miami',
            'region': 'FL',
            'postalCode': '33018',
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
    assert shipment_location.ShipToAddress.city == 'Miami'
    assert shipment_location.ShipToAddress.address1 is None


def test_address_region_can_have_more_than2_chars():
    data = {
        'address1': None,
        'address2': 'Suite B',
        'address3': None,
        'address4': None,
        'city': '',
        'region': 'China',
        'postalCode': None,
        'country': 'China'
    }
    address = Address.model_validate(data)
    assert address.region == 'China'
    assert address.country == 'China'


def test_osn():
    now = datetime.now()
    data = {
        'OrderShipmentNotificationArray': {
            'OrderShipmentNotification': [
                {
                    'purchaseOrderNumber': 'PO-236280',
                    'complete': True,
                    'SalesOrderArray': {
                        'SalesOrder': [
                            {
                                'salesOrderNumber': '52279501',
                                'complete': True,
                                'ShipmentLocationArray': {
                                    'ShipmentLocation': [
                                        {
                                            'id': 12,
                                            'complete': True,
                                            'ShipFromAddress': {
                                                'address1': 'FULFILLMENT SERVICES (SD)',
                                                'address2': '12121 SCRIPPS SUMMIT DR',
                                                'address3': 'SUITE 200',
                                                'address4': None,
                                                'city': 'SAN DIEGO',
                                                'region': 'CA',
                                                'postalCode': '92131',
                                                'country': 'US'
                                            },
                                            'ShipToAddress': {
                                                'address1': 'Gallardo Solutions Corp',
                                                'address2': '.',
                                                'address3': '226 OLD NEW BRUNSWICK RD STE B',
                                                'address4': None,
                                                'city': 'Miami',
                                                'region': 'FL',
                                                'postalCode': '33013',
                                                'country': 'US'
                                            },
                                            'shipmentDestinationType': None,
                                            'PackageArray': {
                                                'Package': [
                                                    {
                                                        'id': 1,
                                                        'trackingNumber': '711456164060',
                                                        'shipmentDate': now,
                                                        'dimUOM': None,
                                                        'length': None,
                                                        'width': None,
                                                        'height': None,
                                                        'weightUOM': 'Pounds',
                                                        'weight': Decimal('8.00'),
                                                        'carrier': 'FEDEX',
                                                        'shipmentMethod': 'FEDEX GROUND',
                                                        'shippingAccount': '539428560',
                                                        'shipmentTerms': None,
                                                        'ItemArray': {
                                                            'Item': [
                                                                None
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                },
                {
                    'purchaseOrderNumber': 'PO-236306',
                    'complete': True,
                    'SalesOrderArray': {
                        'SalesOrder': [
                            {
                                'salesOrderNumber': '52282615',
                                'complete': True,
                                'ShipmentLocationArray': {
                                    'ShipmentLocation': [
                                        {
                                            'id': 12,
                                            'complete': True,
                                            'ShipFromAddress': {
                                                'address1': 'FULFILLMENT SERVICES (SD)',
                                                'address2': '12121 SCRIPPS SUMMIT DR',
                                                'address3': 'SUITE 200',
                                                'address4': None,
                                                'city': 'SAN DIEGO',
                                                'region': 'CA',
                                                'postalCode': '92131',
                                                'country': 'US'
                                            },
                                            'ShipToAddress': {
                                                'address1': 'Gallardo Solutions Corp',
                                                'address2': '.',
                                                'address3': '226 OLD NEW BRUNSWICK RD STE B',
                                                'address4': None,
                                                'city': 'Hialeah',
                                                'region': 'FL',
                                                'postalCode': '33018',
                                                'country': 'US'
                                            },
                                            'shipmentDestinationType': None,
                                            'PackageArray': {
                                                'Package': [
                                                    {
                                                        'id': 1,
                                                        'trackingNumber': '1Z1812320321855099',
                                                        'shipmentDate': now,
                                                        'dimUOM': None,
                                                        'length': None,
                                                        'width': None,
                                                        'height': None,
                                                        'weightUOM': 'Pounds',
                                                        'weight': Decimal('3.00'),
                                                        'carrier': 'UPS',
                                                        'shipmentMethod': 'UPS GROUND',
                                                        'shippingAccount': '81R3Y3',
                                                        'shipmentTerms': None,
                                                        'ItemArray': {
                                                            'Item': [
                                                                None
                                                            ]
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        },
        'ErrorMessage': None
    }
    resp = GetOrderShipmentNotificationResponse.model_validate(data)
    assert resp.OrderShipmentNotificationArray.OrderShipmentNotification[0].purchaseOrderNumber == 'PO-236280'
