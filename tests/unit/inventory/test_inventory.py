# flake8: noqa F811
from decimal import Decimal

import xmltodict

from psdomain.model import InventoryLevelsResponseV121
from psdomain.model.inventory.v_2_0_0 import ZERO, InventoryLevelsResponseV200
from psdomain.model.base import Severity

from .fixtures import inventory_2_0_0_ok_obj, inventory_1_2_1_ok_obj  # noqa
from .responses.v_2_0_0 import inventory_2_0_0_error_response, inventory_2_0_0_error_response_2
from .responses.v_1_2_1 import storm_tech_response


def parse_xml(text: str):
    return xmltodict.parse(
            text, encoding='utf-8', process_namespaces=False,
            namespaces={f'ns{i}': None for i in range(20)}
        )


def test_parts_2_0_0(inventory_2_0_0_ok_obj):
    parts = set(inventory_2_0_0_ok_obj.parts)
    expected_parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
                      '50078RPNK', '50078RPUR'}
    assert parts.intersection(expected_parts) == expected_parts


def test_parts_1_0_0(inventory_1_2_1_ok_obj):
    parts = set(inventory_1_2_1_ok_obj.parts)
    expected_parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
                      '50078RPNK', '50078RPUR'}
    assert parts.intersection(expected_parts) == expected_parts


def test_get_available_inventory_2_0_0(inventory_2_0_0_ok_obj):
    get_available_inventory = inventory_2_0_0_ok_obj.get_available_inventory
    lst = [
        ('50078RBLK', Decimal(33018)),
        ('50078RWHT', Decimal(33375)),
        ('50078RNAV', Decimal(27684)),
        ('50078RRED', Decimal(5112)),
        ('50078RBLU', Decimal(14306)),
        ('50078RLIM', ZERO),
        ('50078RORN', ZERO),
        ('50078RPNK', ZERO),
        ('50078RPUR', ZERO),
    ]
    for part_id, expected in lst:
        assert get_available_inventory(part_id) == expected


def test_get_available_inventory_1_2_1(inventory_1_2_1_ok_obj):
    get_available_inventory = inventory_1_2_1_ok_obj.get_available_inventory
    lst = [
        ('50078RBLK', Decimal(32717)),
        ('50078RWHT', Decimal(32550)),
        ('50078RNAV', Decimal(27634)),
        ('50078RRED', Decimal(5043)),
        ('50078RBLU', Decimal(27813)),
        ('50078RLIM', ZERO),
        ('50078RORN', ZERO),
        ('50078RPNK', ZERO),
        ('50078RPUR', ZERO),
    ]
    for part_id, expected in lst:
        assert get_available_inventory(part_id) == expected


def test_get_incoming_inventory_2_0_0(inventory_2_0_0_ok_obj):
    get_incoming_inventory = inventory_2_0_0_ok_obj.get_incoming_inventory
    #                                         }
    assert get_incoming_inventory('50078RBLK') == Decimal(
        26288 + 41288 + 48288 + 53240 + 58240 + 68240 + 83240 + 98240 + 113240
    )
    assert get_incoming_inventory('50078RWHT') == Decimal(
        31339 + 44644 + 45064 + 45484 + 45904 + 50750 + 65750 + 66750 + 75750 + 80750 + 95750 + 100750
    )


def test_get_incoming_inventory_1_2_1(inventory_1_2_1_ok_obj):
    obj = inventory_1_2_1_ok_obj
    for part_id in obj.parts:
        assert obj.get_incoming_inventory(part_id) == ZERO


def test_error_in_inventory_2_0_0():
    obj = InventoryLevelsResponseV200.model_validate_json(inventory_2_0_0_error_response)
    assert obj.Inventory is None
    msg = obj.ServiceMessageArray.ServiceMessage[0]
    assert msg.code == 610
    assert msg.severity == Severity.ERROR


def test_error_in_inventory_2_0_0_2():
    obj = InventoryLevelsResponseV200.model_validate(inventory_2_0_0_error_response_2)
    assert obj.Inventory is None
    msg = obj.ServiceMessageArray.ServiceMessage[0]
    assert msg.code == 160
    assert msg.severity == Severity.ERROR
    assert msg.description == 'No Results Found'
    #
    obj1 = InventoryLevelsResponseV200.model_validate(obj)
    assert obj1 == obj


def test_is_manufactured_2_0_0(inventory_2_0_0_ok_obj):
    parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
             '50078RPNK', '50078RPUR'}
    for part_id in parts:
        assert inventory_2_0_0_ok_obj.is_manufactured(part_id) is False


def test_is_manufactured_1_2_1(inventory_1_2_1_ok_obj):
    parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
             '50078RPNK', '50078RPUR'}
    for part_id in parts:
        assert inventory_1_2_1_ok_obj.is_manufactured(part_id) is False


def test_storm_tech_response():
    obj = InventoryLevelsResponseV121.model_validate(storm_tech_response)
    assert obj.errorMessage is None


def test_inventory_121():
    xml = """
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:ns1="http://www.promostandards.org/WSDL/InventoryService/1.0.0/">
        <SOAP-ENV:Body>
            <ns1:Reply>
                <ns1:productID>10R801</ns1:productID>
                <ns1:ProductVariationInventoryArray>
                    <ns1:ProductVariationInventory>
                        <ns1:partID>10R80100BLK                   </ns1:partID>
                        <ns1:partDescription>
                            Premec tip brass plated 0.7mm medium tip rollerball ink refill (black  blue ink color)
                        </ns1:partDescription>
                        <ns1:quantityAvailable>0</ns1:quantityAvailable>
                        <ns1:attributeColor>Black</ns1:attributeColor>
                        <ns1:validTimestamp>2024-01-13T02:09:43Z</ns1:validTimestamp>
                        </ns1:ProductVariationInventory><ns1:ProductVariationInventory>
                        <ns1:partID>10R80100BLU                   </ns1:partID>
                        <ns1:partDescription>
                        Premec tip brass plated 0.7mm medium tip rollerball ink refill (black  blue ink color)
                        </ns1:partDescription>
                        <ns1:quantityAvailable>2974</ns1:quantityAvailable>
                        <ns1:attributeColor>Blue</ns1:attributeColor>
                        <ns1:validTimestamp>2024-01-13T02:09:43Z</ns1:validTimestamp>
                    </ns1:ProductVariationInventory>
                </ns1:ProductVariationInventoryArray>
                </ns1:Reply>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
    """
    parsed = parse_xml(xml)
    data = parsed['SOAP-ENV:Envelope']['SOAP-ENV:Body']['Reply']
    resp = InventoryLevelsResponseV121.model_validate(data)
    assert resp.productID == '10R801'
    first = resp.ProductVariationInventoryArray.ProductVariationInventory[0]
    assert first.partID == '10R80100BLK'
    assert first.partDescription == 'Premec tip brass plated 0.7mm medium tip rollerball ink refill (black  blue ink color)'  # noqa
    assert first.quantityAvailable == '0'


def test_inventory_v121_soap_client():
    data = {
        'productID': '10P901',
        'ProductVariationInventoryArray': {
            'ProductVariationInventory': [
                {
                    'partID': '10P90100BLK',
                    'partDescription': 'Brass plated metal premec 1.0mm ink medium tip refill (black  blue ink color)',
                    'partBrand': None,
                    'priceVariance': None,
                    'quantityAvailable': '10004',
                    'attributeColor': 'Black',
                    'attributeSize': None,
                    'attributeSelection': None,
                    'AttributeFlexArray': None,
                    'customProductMessage': None,
                    'entryType': None,
                    'validTimestamp': '2024-01-13T02:56:49+00:00'
                },
                {
                    'partID': '10P90100BLU',
                    'partDescription': 'Brass plated metal premec 1.0mm ink medium tip refill (black  blue ink color)',
                    'partBrand': None,
                    'priceVariance': None,
                    'quantityAvailable': '9000',
                    'attributeColor': 'Blue',
                    'attributeSize': None,
                    'attributeSelection': None,
                    'AttributeFlexArray': None,
                    'customProductMessage': None,
                    'entryType': None,
                    'validTimestamp': '2024-01-13T02:56:49+00:00'
                }
            ]
        }
    }
    resp = InventoryLevelsResponseV121.model_validate(data)
    assert resp.productID == '10P901'
    first = resp.ProductVariationInventoryArray.ProductVariationInventory[0]
    assert first.partID == '10P90100BLK'
    assert first.quantityAvailable == '10004'
    assert first.attributeColor == 'Black'
    second = resp.ProductVariationInventoryArray.ProductVariationInventory[1]
    assert second.partID == '10P90100BLU'
    assert second.quantityAvailable == '9000'
    assert second.attributeColor == 'Blue'
