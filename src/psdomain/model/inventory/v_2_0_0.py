from decimal import Decimal
from datetime import datetime
from typing import Annotated

from pydantic import model_validator

from .. import base
from ..base import StrEnum

PSBaseModel = base.PSBaseModel


ZERO = Decimal(0)


class LabelSize(StrEnum):
    """
    The apparel items tagged size.
    Enumerated values: {6XS,5XS,4XS,3XS,2XS,XS,S,M,L,XL,2XL,3XL,4XL,5XL,6XL,CUSTOM}

    CUSTOM is used for any size that does not match one of the other sizes. For example 7XL and 8XL would return CUSTOM.
    To identify the actual size when CUSTOM is returned, reference the Product Data endpoint.
    """
    SIX_XS = '6XS'
    FIVE_XS = '5XS'
    FOUR_XS = '4XS'
    THREE_XS = '3XS'
    TWOS_XS = '2XS'
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    TWO_L = '2XL'
    THREE_L = '3XL'
    FOUR_L = '4XL'
    FIVE_L = '5XL'
    SIXL = '6XL'
    CUSTOM = 'CUSTOM'


class Quantity(PSBaseModel):
    value: Decimal
    uom: base.UOM


class QuantityAvailable(PSBaseModel):
    Quantity: Quantity

    @property
    def value(self) -> Decimal:
        return self.Quantity.value


class FutureAvailability(PSBaseModel):
    Quantity: Quantity
    availableOn: datetime

    @property
    def value(self) -> Decimal:
        return self.Quantity.value


class FutureAvailabilityArray(PSBaseModel):
    FutureAvailability: list[FutureAvailability]

    @property
    def value(self) -> Decimal:
        return sum([fa.value for fa in self.FutureAvailability], ZERO)


class Address(PSBaseModel):
    city: str | None
    country: str | None
    postalCode: str | None


class InventoryLocation(PSBaseModel):
    inventoryLocationId: str
    inventoryLocationName: str | None
    postalCode: str | None = ...  # the doc says it required but HIT fails if it is
    country: str | None = ...     # the doc says it required but HIT fails if it is
    inventoryLocationQuantity: QuantityAvailable | None
    FutureAvailabilityArray: FutureAvailabilityArray | None

    @property
    def future_availability(self) -> Decimal:
        return self.FutureAvailabilityArray.value if self.FutureAvailabilityArray else ZERO

    @property
    def current_availability(self) -> Decimal:
        return self.inventoryLocationQuantity.value if self.inventoryLocationQuantity else ZERO


class InventoryLocationArray(PSBaseModel):
    InventoryLocation: list[InventoryLocation]

    @property
    def future_availability(self) -> Decimal:
        return sum([loc.future_availability for loc in self.InventoryLocation], ZERO)

    @property
    def current_availability(self) -> Decimal:
        return sum([loc.current_availability for loc in self.InventoryLocation], ZERO)


class PartInventory(PSBaseModel):
    partId: str
    mainPart: bool
    partColor: str | None = None
    labelSize: str | None = None
    partDescription: str | None = None
    quantityAvailable: QuantityAvailable | None
    manufacturedItem: bool
    buyToOrder: bool
    replenishmentLeadTime: int | None = None
    attributeSelection: str | None
    lastModified: datetime | None = None
    InventoryLocationArray: InventoryLocationArray | None

    @property
    def inventory_location(self):
        return self.InventoryLocationArray.InventoryLocation if self.InventoryLocationArray else []

    @property
    def current_availability(self) -> Decimal:
        if self.quantityAvailable:
            return self.quantityAvailable.value
        return sum([loc.current_availability for loc in self.inventory_location], ZERO)

    @property
    def future_availability(self) -> Decimal:
        return sum([loc.future_availability for loc in self.inventory_location], ZERO)


class PartInventoryArray(PSBaseModel):
    PartInventory: list[PartInventory]

    @classmethod
    def empty(cls):
        return cls(PartInventory=[])


class Inventory(PSBaseModel):
    productId: str
    PartInventoryArray: Annotated[PartInventoryArray, None]

    @property
    def part_inventory(self):
        return self.PartInventoryArray.PartInventory if self.PartInventoryArray else []


class ArrayOfLabelSize(PSBaseModel):
    labelSize: list[str]


class ArrayOfPartColor(PSBaseModel):
    partColor: list[str]


class ArrayOfPartId(PSBaseModel):
    partId: list[str]


class Filter(PSBaseModel):
    partIdArray: ArrayOfPartId | None
    LabelSizeArray: ArrayOfLabelSize | None
    PartColorArray: ArrayOfPartColor | None


class FilterValues(PSBaseModel):
    productId: str | None = None
    Filter: Filter

    @model_validator(mode='before')
    def upgrade_filter(cls, values):
        try:
            if isinstance(values, list):
                parts, sizes, colors = [], [], []
                self = values[0]
                arr = self['FilterArray']
                del self['FilterArray']
                lst = arr['Filter']
                for v in lst:
                    if v['partId']:
                        parts.append(v['partId'])
                    size_arr = v['LabelSizeArray']
                    if size_arr:
                        sizes.extend(size_arr['labelSize'])
                    color_arr = v['PartColorArray']
                    if color_arr:
                        colors.extend(color_arr['partColor'])
                self['Filter'] = {
                    'partIdArray': {'partId': parts} if parts else None,
                    'LabelSizeArray': {'labelSize': sizes} if sizes else None,
                    'PartColorArray': {'partColor': colors} if colors else None
                }
                return self
        except ValueError:
            raise ValueError(f"Invalid Filter value: {values}")
        return values


class ProductIDType(StrEnum):
    """
    The type of product ID to search for.
    """
    Distributor = 'Distributor'
    Supplier = 'Supplier'


class FilterValuesResponseV200(PSBaseModel):
    FilterValues: FilterValues | None
    ServiceMessageArray: base.ServiceMessageArray | None


class InventoryLevelsResponseV200(PSBaseModel):
    Inventory: Inventory | None  # An object containing the inventory levels for the given product
    ServiceMessageArray: base.ServiceMessageArray | None

    def get_available_inventory(self, part_id: str) -> Decimal:
        pi = self.part_inventory_dict.get(part_id)
        return pi.current_availability if pi else ZERO

    def get_incoming_inventory(self, part_id: str) -> Decimal:
        pi = self.part_inventory_dict.get(part_id)
        return pi.future_availability if pi else ZERO

    @property
    def part_inventory_dict(self):
        ret = getattr(self, '_part_inventory_dict', None)
        if ret is None:
            setattr(self, '_part_inventory_dict', self.gen_part_inventory_dict())
            ret = self._part_inventory_dict
        return ret

    def gen_part_inventory_dict(self):
        return {pi.partId: pi for pi in self.part_inventory}

    @property
    def part_inventory(self) -> list[PartInventory]:
        return self.Inventory.part_inventory if self.Inventory else []

    @property
    def parts(self) -> list[str]:
        return list({pi.partId for pi in self.part_inventory})
