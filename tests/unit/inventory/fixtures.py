import pytest

from psdomain.model.inventory.v_2_0_0 import InventoryLevelsResponseV200
from psdomain.model.inventory.v_1_2_1 import InventoryLevelsResponseV121
from .responses.v_1_2_1 import inventory_1_2_1_ok_response
from .responses.v_2_0_0 import inventory_2_0_0_ok_response


@pytest.fixture
def inventory_2_0_0_ok_obj() -> InventoryLevelsResponseV200:
    yield InventoryLevelsResponseV200.model_validate(inventory_2_0_0_ok_response)


@pytest.fixture
def inventory_1_2_1_ok_obj() -> InventoryLevelsResponseV121:
    yield InventoryLevelsResponseV121.model_validate(inventory_1_2_1_ok_response)
