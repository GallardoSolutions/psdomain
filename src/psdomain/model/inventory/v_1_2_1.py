from datetime import datetime
from typing import List, Optional, Annotated
from decimal import Decimal

from pydantic import constr, field_validator, Field

from ..base import PSBaseModel, ZERO


class AttributeFlex(PSBaseModel):
    id: constr(max_length=64)
    name: constr(max_length=64)
    value: constr(max_length=256)


class AttributeFlexArray(PSBaseModel):
    AttributeFlex: List[AttributeFlex]

    @field_validator('AttributeFlex', mode="before")
    def validate_attribute_flex(cls, v):
        if v is None:
            return []
        if not isinstance(v, list):
            return [v]
        return v


class ProductVariationInventory(PSBaseModel):
    partID: constr(max_length=64)
    partDescription: Optional[constr(max_length=256)] = None
    partBrand: Optional[constr(max_length=64)] = None
    priceVariance: Optional[constr(max_length=64)] = None
    quantityAvailable: constr(max_length=64)
    attributeColor: Optional[constr(max_length=64)] = None
    attributeSize: Optional[constr(max_length=64)] = None
    attributeSelection: Optional[constr(max_length=64)] = None
    AttributeFlexArray: Annotated[Optional[AttributeFlexArray], Field(None)]
    customProductMessage: Optional[constr(max_length=256)] = None
    entryType: Optional[constr(max_length=64)] = None
    validTimestamp: Optional[datetime] = None

    @field_validator('AttributeFlexArray', mode="before")
    def validate_attribute_flex_array(cls, v):
        # Handle None values
        if v is None:
            return None
        # Handle empty values that should be None
        if isinstance(v, dict):
            if not v or 'AttributeFlex' not in v:
                return None
            if v.get('AttributeFlex') in [None, [], {}]:
                return None
            # Valid data - pass through for AttributeFlexArray validation
            return v
        # Handle empty lists
        if isinstance(v, list) and len(v) == 0:
            return None
        return v

    @property
    def value(self):
        return Decimal(self.quantityAvailable) if self.quantityAvailable else ZERO

    @property
    def current_availability_v1(self) -> Decimal:
        return self.value

    @property
    def current_availability_v2(self) -> Decimal:
        return self.current_availability_v1


class ProductVariationInventoryArray(PSBaseModel):
    ProductVariationInventory: List[ProductVariationInventory]

    @field_validator('ProductVariationInventory', mode="before")
    def check_product_variation_inventory(cls, v, values, **kwargs):
        if isinstance(v, dict):
            return [v]
        return v

    @property
    def inventory_location(self):
        return []


class ProductCompanionInventory(PSBaseModel):
    partID: constr(max_length=64)
    partDescription: Optional[constr(max_length=256)] = None
    partBrand: Optional[constr(max_length=64)] = None
    price: Optional[constr(max_length=64)] = None
    quantityAvailable: constr(max_length=64)
    attributeColor: Optional[constr(max_length=64)] = None
    attributeSize: Optional[constr(max_length=64)] = None
    attributeSelection: Optional[constr(max_length=64)] = None
    entryType: Optional[constr(max_length=64)] = None
    AttributeFlexArray: Annotated[Optional[AttributeFlexArray], Field(None)]
    customProductMessage: Optional[constr(max_length=256)] = None
    validTimestamp: Optional[datetime] = None

    @field_validator('AttributeFlexArray', mode="before")
    def validate_attribute_flex_array(cls, v):
        # Handle None values
        if v is None:
            return None
        # Handle empty values that should be None
        if isinstance(v, dict):
            if not v or 'AttributeFlex' not in v:
                return None
            if v.get('AttributeFlex') in [None, [], {}]:
                return None
            # Valid data - pass through for AttributeFlexArray validation
            return v
        # Handle empty lists
        if isinstance(v, list) and len(v) == 0:
            return None
        return v


class CustomMessage(PSBaseModel):
    # Define the structure of each item in CustomMessageArray
    pass  # Replace with actual fields


class ProductCompanionInventoryArray(PSBaseModel):
    ProductCompanionInventory: List[ProductCompanionInventory]


class InventoryLevelsResponseV121(PSBaseModel):
    productID: constr(max_length=64)
    ProductVariationInventoryArray: Optional[ProductVariationInventoryArray]
    ProductCompanionInventoryArray: Optional[ProductCompanionInventoryArray] = None
    errorMessage: Optional[constr(max_length=256)] = None
    CustomMessageArray: Optional[List[CustomMessage]] = None
    errorMessage: str | None

    @property
    def is_ok(self):
        return self.errorMessage is None

    @property
    def errors(self):
        return self.errorMessage if self.errorMessage else None

    @field_validator('ProductVariationInventoryArray', mode="before")
    def check_product_variation_inventory_array(cls, v, values, **kwargs):
        if not v:
            return None
        return v

    @property
    def parts(self) -> list[str]:
        return list({pi.partID for pi in self.part_inventory})

    @property
    def part_inventory_dict(self):
        ret = getattr(self, '_part_inventory_dict', None)
        if ret is None:
            setattr(self, '_part_inventory_dict', self.gen_part_inventory_dict())
            ret = self._part_inventory_dict
        return ret

    def gen_part_inventory_dict(self):
        # Some suppliers like Quickey have different casing in the Product data and Inventory data
        return {pi.partID.upper(): pi for pi in self.part_inventory if pi.partID is not None}

    @property
    def part_inventory(self) -> List[ProductVariationInventory]:
        if self.ProductVariationInventoryArray:
            return self.ProductVariationInventoryArray.ProductVariationInventory
        return []

    def get_available_inventory(self, part_id: str) -> Decimal:
        return sum([int(pi.value)
                    for pi in self.part_inventory
                    if pi.partID and pi.partID.upper() == part_id.upper()],
                   ZERO)

    @staticmethod
    def get_incoming_inventory(part_id: str) -> Decimal:
        return ZERO

    @staticmethod
    def is_manufactured(part_id: str) -> bool:
        return False  # In this version, we don't know
