"""OSN 2.0.0 answers validate the way suppliers really send them.

The 2.0.0 schema spells shipFromAddress, shipToAddress and Quantity (the model keeps the 1.0.0-style
ShipFromAddress, ShipToAddress and quantity in its output), and Lincoln Line sends a ship-from address
without a postalCode and attentionTo values longer than 35 characters. None of it may reject the response.
All data here is made up.
"""
from types import SimpleNamespace

from psdomain.model.osn.v_2_0_0 import GetOrderShipmentNotificationResponseV200, Item, Shipment, \
    ShippingContactDetails

SHIP_FROM = {
    'attentionTo': None,
    'companyName': 'Example Warehouse',
    'address1': '100 Example Way',
    'address2': None,
    'address3': None,
    'city': 'Springfield',
    'region': 'IL',
    'postalCode': None,
    'country': 'US',
    'email': None,
    'phone': None,
}

SHIP_TO = {
    'attentionTo': 'REF: 000000 / JANE EXAMPLE / PO-000000',
    'companyName': 'Example Customer',
    'address1': '200 Sample Street',
    'address2': 'Suite 9',
    'address3': None,
    'city': 'Shelbyville',
    'region': 'TN',
    'postalCode': '37160',
    'country': 'US',
    'email': 'receiving@example.com',
    'phone': '555-0100',
}


def item(**quantity):
    return {
        'supplierProductId': 'P-1',
        'supplierPartId': 'P-1-RED',
        'distributorProductId': None,
        'distributorPartId': None,
        'purchaseOrderLineNumber': 1,
        **quantity,
    }


def shipment(**addresses):
    return {
        'destinationShippedInFull': True,
        'customerPickup': False,
        'shipmentDestinationType': None,
        'PackageArray': {'Package': [{
            'id': 1,
            'trackingNumber': '1Z0000000000000000',
            'shipmentDate': '2026-11-19T00:00:00',
            'Dimension': None,
            'FreightDetails': {'carrier': 'UPS', 'service': 'Ground'},
            'shippingAccount': None,
            'shipmentTerms': None,
            'ItemArray': {'Item': [item(Quantity={'value': '500', 'uom': 'EA'})]},
            'preProductionProof': None,
        }]},
        **addresses,
    }


def response(*shipments):
    return {
        'OrderShipmentNotificationArray': {'OrderShipmentNotification': [{
            'purchaseOrderNumber': 'PO-000000',
            'purchaseOrderShippedInFull': True,
            'SalesOrderArray': {'SalesOrder': [{
                'salesOrderNumber': 'SO-1',
                'salesOrderShippedInFull': True,
                'ShipmentArray': {'Shipment': list(shipments)},
            }]},
        }]},
        'ServiceMessageArray': None,
    }


def test_spec_shaped_response_validates_and_keeps_the_model_names_in_its_output():
    resp = GetOrderShipmentNotificationResponseV200.model_validate(
        response(shipment(shipFromAddress=SHIP_FROM, shipToAddress=SHIP_TO)))

    sh = resp.OrderShipmentNotificationArray.OrderShipmentNotification[0].SalesOrderArray.SalesOrder[0] \
        .ShipmentArray.Shipment[0]
    assert sh.ShipFromAddress.companyName == 'Example Warehouse'
    assert sh.ShipToAddress.postalCode == '37160'
    assert sh.PackageArray.Package[0].ItemArray.Item[0].quantity.value == 500

    dumped = resp.model_dump(mode='json')
    sh_json = dumped['OrderShipmentNotificationArray']['OrderShipmentNotification'][0]['SalesOrderArray'][
        'SalesOrder'][0]['ShipmentArray']['Shipment'][0]
    assert {'ShipFromAddress', 'ShipToAddress'} <= sh_json.keys()
    assert not {'shipFromAddress', 'shipToAddress'} & sh_json.keys()
    item_json = sh_json['PackageArray']['Package'][0]['ItemArray']['Item'][0]
    assert 'quantity' in item_json and 'Quantity' not in item_json


def test_model_names_still_validate():
    resp = GetOrderShipmentNotificationResponseV200.model_validate(
        response(shipment(ShipFromAddress=SHIP_FROM, ShipToAddress=SHIP_TO)))
    sh = resp.OrderShipmentNotificationArray.OrderShipmentNotification[0].SalesOrderArray.SalesOrder[0] \
        .ShipmentArray.Shipment[0]
    assert sh.ShipToAddress.city == 'Shelbyville'
    assert Item.model_validate(item(quantity={'value': '3', 'uom': 'EA'})).quantity.value == 3


def test_model_name_wins_when_both_spellings_are_present():
    other = {**SHIP_TO, 'city': 'Capital City'}
    sh = Shipment.model_validate(shipment(ShipToAddress=SHIP_TO, shipToAddress=other, ShipFromAddress=SHIP_FROM))
    assert sh.ShipToAddress.city == 'Shelbyville'

    it = Item.model_validate(item(quantity={'value': '1', 'uom': 'EA'}, Quantity={'value': '2', 'uom': 'EA'}))
    assert it.quantity.value == 1


def test_spec_names_are_read_from_attributes_too():
    # psrestful-api validates zeep objects (from_attributes): an attribute that is missing raises AttributeError
    # there, like it does on a SimpleNamespace.
    it = Item.model_validate(SimpleNamespace(**item(Quantity=SimpleNamespace(value='7', uom='EA'))))
    assert it.quantity.value == 7


def test_ship_from_address_without_postal_code_validates():
    address = ShippingContactDetails.model_validate(SHIP_FROM)
    assert address.postalCode is None


def test_contact_details_keep_supplier_values_longer_than_the_spec_limits():
    long_values = {
        'attentionTo': 'REF: 000000 / JANE EXAMPLE / PO-000000',
        'companyName': 'An Example Company Name That Is Much Longer Than Thirty Five',
        'address1': '1234 A Very Long Example Street Name Boulevard',
        'city': 'A City Name Longer Than Thirty Characters',
        'region': 'Tennessee',
        'postalCode': '37160-0000-00',
        'country': 'USA',
        'phone': '+1 (555) 010-0000 extension 123456789',
    }
    address = ShippingContactDetails.model_validate({**SHIP_TO, **long_values})
    assert address.model_dump(include=set(long_values)) == long_values


def test_contact_details_with_every_field_missing_validate():
    address = ShippingContactDetails.model_validate({})
    assert address.model_dump() == dict.fromkeys(ShippingContactDetails.model_fields)


def test_country_keeps_its_value_in_json():
    assert ShippingContactDetails.model_validate(SHIP_TO).model_dump(mode='json')['country'] == 'US'
