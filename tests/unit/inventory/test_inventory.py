# flake8: noqa F811
from decimal import Decimal

import xmltodict

from psdomain.model import InventoryLevelsResponseV121
from psdomain.model.inventory.v_2_0_0 import ZERO, InventoryLevelsResponseV200
from psdomain.model.base import Severity

from .fixtures import inventory_2_0_0_ok_obj, inventory_1_2_1_ok_obj  # noqa
from .responses.v_2_0_0 import inventory_2_0_0_error_response, inventory_2_0_0_error_response_2, \
    inventory_2_0_0_error_response_from_xml_to_dict
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


def test_part_inventory_dict_1_2_1(inventory_1_2_1_ok_obj):
    """Test that part_inventory_dict property works correctly in v1.2.1"""
    # Access the part_inventory_dict property
    part_dict = inventory_1_2_1_ok_obj.part_inventory_dict

    # Verify it returns a dictionary
    assert isinstance(part_dict, dict)

    # Verify it has the expected parts (keys should be uppercase)
    expected_parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
                      '50078RPNK', '50078RPUR'}
    assert set(part_dict.keys()).intersection(expected_parts) == expected_parts

    # Verify we can look up items by part ID (uppercase)
    black_part = part_dict.get('50078RBLK')
    assert black_part is not None
    assert black_part.partID == '50078RBLK'
    assert black_part.quantityAvailable == '32717'

    # Verify case-insensitive lookup works (keys are uppercase)
    assert part_dict.get('50078RBLK') is not None
    assert part_dict.get('50078rblk') is None  # lowercase should not work directly

    # Test caching behavior - calling property again should return same object
    part_dict_2 = inventory_1_2_1_ok_obj.part_inventory_dict
    assert part_dict is part_dict_2  # Same object reference due to caching


def test_part_inventory_dict_2_0_0(inventory_2_0_0_ok_obj):
    """Test that part_inventory_dict property works correctly in v2.0.0"""
    # Access the part_inventory_dict property
    part_dict = inventory_2_0_0_ok_obj.part_inventory_dict

    # Verify it returns a dictionary
    assert isinstance(part_dict, dict)

    # Verify it has the expected parts (keys should be uppercase)
    expected_parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
                      '50078RPNK', '50078RPUR'}
    assert set(part_dict.keys()).intersection(expected_parts) == expected_parts

    # Verify we can look up items by part ID (uppercase)
    black_part = part_dict.get('50078RBLK')
    assert black_part is not None
    assert black_part.partId == '50078RBLK'
    assert black_part.current_availability == Decimal(33018)

    # Test caching behavior - calling property again should return same object
    part_dict_2 = inventory_2_0_0_ok_obj.part_inventory_dict
    assert part_dict is part_dict_2  # Same object reference due to caching


def test_current_availability_v1_1_2_1(inventory_1_2_1_ok_obj):
    """Test that current_availability_v1 works correctly in v1.2.1"""
    # Get the part inventory items
    part_inventory = inventory_1_2_1_ok_obj.part_inventory

    # Test with items that have quantity
    black_part = next(pi for pi in part_inventory if pi.partID == '50078RBLK')
    assert black_part.current_availability_v1 == Decimal(32717)
    assert black_part.current_availability_v1 == black_part.value

    white_part = next(pi for pi in part_inventory if pi.partID == '50078RWHT')
    assert white_part.current_availability_v1 == Decimal(32550)

    # Test with items that have zero quantity
    lime_part = next(pi for pi in part_inventory if pi.partID == '50078RLIM')
    assert lime_part.current_availability_v1 == ZERO


def test_current_availability_v2_1_2_1(inventory_1_2_1_ok_obj):
    """Test that current_availability_v2 works in v1.2.1 (should match v1 since no location data)"""
    # Get the part inventory items
    part_inventory = inventory_1_2_1_ok_obj.part_inventory

    # In v1.2.1, current_availability_v2 should equal current_availability_v1
    # because inventory_location is not available (returns empty list)
    black_part = next(pi for pi in part_inventory if pi.partID == '50078RBLK')
    assert black_part.current_availability_v2 == black_part.current_availability_v1
    assert black_part.current_availability_v2 == Decimal(32717)

    white_part = next(pi for pi in part_inventory if pi.partID == '50078RWHT')
    assert white_part.current_availability_v2 == white_part.current_availability_v1
    assert white_part.current_availability_v2 == Decimal(32550)

    lime_part = next(pi for pi in part_inventory if pi.partID == '50078RLIM')
    assert lime_part.current_availability_v2 == lime_part.current_availability_v1
    assert lime_part.current_availability_v2 == ZERO


def test_current_availability_v2_2_0_0_with_locations(inventory_2_0_0_ok_obj):
    """Test that current_availability_v2 calculates from inventory locations in v2.0.0"""
    # Get a part that has inventory locations
    black_part = inventory_2_0_0_ok_obj.part_inventory_dict.get('50078RBLK')
    assert black_part is not None

    # Verify this part has inventory locations
    assert black_part.inventory_location is not None
    assert len(black_part.inventory_location) > 0

    # current_availability_v2 should sum all location quantities
    expected_v2 = sum([loc.current_availability for loc in black_part.inventory_location], ZERO)
    assert black_part.current_availability_v2 == expected_v2
    assert black_part.current_availability_v2 == Decimal(33018)

    # Test another part
    white_part = inventory_2_0_0_ok_obj.part_inventory_dict.get('50078RWHT')
    assert white_part is not None
    assert len(white_part.inventory_location) > 0
    assert white_part.current_availability_v2 == Decimal(33375)


def test_current_availability_v2_2_0_0_without_locations():
    """Test that current_availability_v2 falls back to quantityAvailable when no locations"""
    from psdomain.model.inventory.v_2_0_0 import PartInventory, QuantityAvailable, Quantity
    from psdomain.model.base import UOM

    # Create a part with quantityAvailable but no inventory locations
    part = PartInventory(
        partId='TEST001',
        mainPart=True,
        quantityAvailable=QuantityAvailable(
            Quantity=Quantity(value=Decimal(100), uom=UOM.BX)
        ),
        manufacturedItem=False,
        buyToOrder=False,
        attributeSelection=None,
        InventoryLocationArray=None  # No location data
    )

    # current_availability_v2 should fall back to quantityAvailable
    assert part.current_availability_v2 == Decimal(100)
    assert part.inventory_location == []


def test_current_availability_v2_2_0_0_priority():
    """Test that current_availability_v2 prioritizes location data over quantityAvailable"""
    from psdomain.model.inventory.v_2_0_0 import (
        PartInventory, QuantityAvailable, Quantity, InventoryLocation, InventoryLocationArray
    )
    from psdomain.model.base import UOM

    # Create a part with both quantityAvailable and location data
    part = PartInventory(
        partId='TEST002',
        mainPart=True,
        quantityAvailable=QuantityAvailable(
            Quantity=Quantity(value=Decimal(100), uom=UOM.BX)
        ),
        manufacturedItem=False,
        buyToOrder=False,
        attributeSelection=None,
        InventoryLocationArray=InventoryLocationArray(
            InventoryLocation=[
                InventoryLocation(
                    inventoryLocationId='LOC1',
                    inventoryLocationName='Warehouse 1',
                    postalCode='12345',
                    country='US',
                    inventoryLocationQuantity=QuantityAvailable(
                        Quantity=Quantity(value=Decimal(50), uom=UOM.BX)
                    ),
                    FutureAvailabilityArray=None
                ),
                InventoryLocation(
                    inventoryLocationId='LOC2',
                    inventoryLocationName='Warehouse 2',
                    postalCode='67890',
                    country='US',
                    inventoryLocationQuantity=QuantityAvailable(
                        Quantity=Quantity(value=Decimal(75), uom=UOM.BX)
                    ),
                    FutureAvailabilityArray=None
                )
            ]
        )
    )

    # current_availability_v2 should use location sum (50 + 75 = 125) NOT quantityAvailable (100)
    # This is the key difference - v2 prioritizes location data as it's more reliable
    assert part.current_availability_v2 == Decimal(125)
    assert part.quantityAvailable.value == Decimal(100)  # Original value is different


def test_current_availability_v1_v2_comparison_1_2_1():
    """Test that v1 and v2 are identical in version 1.2.1 API"""
    from psdomain.model.inventory.v_1_2_1 import ProductVariationInventory

    # Create a part with quantity available
    part = ProductVariationInventory(
        partID='TEST003',
        quantityAvailable='500'
    )

    # In v1.2.1, both should be identical since no location support
    assert part.current_availability_v1 == Decimal(500)
    assert part.current_availability_v2 == Decimal(500)
    assert part.current_availability_v1 == part.current_availability_v2


def test_from_xml_to_dict():
    resp = inventory_2_0_0_error_response_from_xml_to_dict['s:Envelope']['s:Body']['GetInventoryLevelsResponse']
    result = InventoryLevelsResponseV200.model_validate(resp)
    assert result.ServiceMessageArray is None


def test_part_inventory_coerce_null_booleans():
    """Test that None boolean fields are coerced to sensible defaults."""
    from psdomain.model.inventory.v_2_0_0 import PartInventory

    part = PartInventory.model_validate({
        'partId': 'TEST-NULL',
        'mainPart': None,
        'manufacturedItem': None,
        'buyToOrder': None,
    })
    assert part.mainPart is True
    assert part.manufacturedItem is False
    assert part.buyToOrder is False


def test_part_inventory_explicit_booleans_preserved():
    """Test that explicit boolean values are not overwritten by the validator."""
    from psdomain.model.inventory.v_2_0_0 import PartInventory

    part = PartInventory.model_validate({
        'partId': 'TEST-EXPLICIT',
        'mainPart': False,
        'manufacturedItem': True,
        'buyToOrder': True,
    })
    assert part.mainPart is False
    assert part.manufacturedItem is True
    assert part.buyToOrder is True
