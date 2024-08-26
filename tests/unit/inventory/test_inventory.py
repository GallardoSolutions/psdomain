# flake8: noqa F811
from decimal import Decimal

from psdomain.model.inventory.v_2_0_0 import ZERO
from .fixtures import inventory_2_0_0_ok_obj  # noqa


def test_parts(inventory_2_0_0_ok_obj):
    parts = set(inventory_2_0_0_ok_obj.parts)
    expected_parts = {'50078RBLK', '50078RWHT', '50078RNAV', '50078RRED', '50078RBLU', '50078RLIM', '50078RORN',
                      '50078RPNK', '50078RPUR'}
    assert parts.intersection(expected_parts) == expected_parts


def test_get_available_inventory(inventory_2_0_0_ok_obj):
    get_available_inventory = inventory_2_0_0_ok_obj.get_available_inventory
    assert get_available_inventory('50078RBLK') == Decimal(33018)
    assert get_available_inventory('50078RWHT') == Decimal(33375)
    assert get_available_inventory('50078RNAV') == Decimal(27684)
    assert get_available_inventory('50078RRED') == Decimal(5112)
    assert get_available_inventory('50078RBLU') == Decimal(14306)
    assert get_available_inventory('50078RLIM') == ZERO
    assert get_available_inventory('50078RORN') == ZERO
    assert get_available_inventory('50078RPNK') == ZERO
    assert get_available_inventory('50078RPUR') == ZERO


def test_get_incoming_inventory(inventory_2_0_0_ok_obj):
    get_incoming_inventory = inventory_2_0_0_ok_obj.get_incoming_inventory
    #                                         }
    assert get_incoming_inventory('50078RBLK') == Decimal(
        26288 + 41288 + 48288 + 53240 + 58240 + 68240 + 83240 + 98240 + 113240
    )
    assert get_incoming_inventory('50078RWHT') == Decimal(
        31339 + 44644 + 45064 + 45484 + 45904 + 50750 + 65750 + 66750 + 75750 + 80750 + 95750 + 100750
    )
