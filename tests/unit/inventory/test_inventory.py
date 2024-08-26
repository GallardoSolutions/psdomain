# flake8: noqa F811
from decimal import Decimal

from psdomain.model.inventory.v_2_0_0 import ZERO, InventoryLevelsResponseV200
from psdomain.model.base import Severity

from .fixtures import inventory_2_0_0_ok_obj, inventory_1_2_1_ok_obj  # noqa
from .responses.v_2_0_0 import inventory_2_0_0_error_response


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
