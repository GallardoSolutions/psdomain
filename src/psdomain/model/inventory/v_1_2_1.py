from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from pydantic import constr, field_validator

from ..base import PSBaseModel, ZERO


class AttributeFlex(PSBaseModel):
    ID: constr(max_length=64)
    Name: constr(max_length=64)
    Value: constr(max_length=256)


class AttributeFlexArray(PSBaseModel):
    AttributeFlex: List[AttributeFlex]


class ProductVariationInventory(PSBaseModel):
    partID: constr(max_length=64)
    partDescription: Optional[constr(max_length=256)] = None
    partBrand: Optional[constr(max_length=64)] = None
    priceVariance: Optional[constr(max_length=64)] = None
    quantityAvailable: constr(max_length=64)
    attributeColor: Optional[constr(max_length=64)] = None
    attributeSize: Optional[constr(max_length=64)] = None
    attributeSelection: Optional[constr(max_length=64)] = None
    AttributeFlexArray: Optional[AttributeFlexArray] = None
    customProductMessage: Optional[constr(max_length=256)] = None
    entryType: Optional[constr(max_length=64)] = None
    validTimestamp: Optional[datetime] = None

    @property
    def value(self):
        return Decimal(self.quantityAvailable) if self.quantityAvailable else ZERO


class ProductVariationInventoryArray(PSBaseModel):
    ProductVariationInventory: List[ProductVariationInventory]

    @field_validator('ProductVariationInventory', mode="before")
    def check_product_variation_inventory(cls, v, values, **kwargs):
        if isinstance(v, dict):
            return [v]
        return v


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
    AttributeFlexArray: Optional[AttributeFlexArray] = None
    customProductMessage: Optional[constr(max_length=256)] = None
    validTimestamp: Optional[datetime] = None


class CustomMessage(PSBaseModel):
    # Define the structure of each item in CustomMessageArray
    pass  # Replace with actual fields


class ProductCompanionInventoryArray(PSBaseModel):
    ProductCompanionInventory: List[ProductCompanionInventory]


class InventoryLevelsResponseV121(PSBaseModel):
    productID: constr(max_length=64)
    ProductVariationInventoryArray: Optional[ProductVariationInventoryArray]
    ProductCompanionInventoryArray: Optional[ProductCompanionInventoryArray] | None = None
    errorMessage: Optional[constr(max_length=256)] = None
    CustomMessageArray: Optional[List[CustomMessage]] = None

    @field_validator('ProductVariationInventoryArray', mode="before")
    def check_product_variation_inventory_array(cls, v, values, **kwargs):
        if not v:
            return None
        return v

    @property
    def parts(self) -> list[str]:
        return list({pi.partID for pi in self.part_inventory})

    @property
    def part_inventory(self) -> List[ProductVariationInventory]:
        if self.ProductVariationInventoryArray:
            return self.ProductVariationInventoryArray.ProductVariationInventory
        return []

    def get_available_inventory(self, part_id: str) -> Decimal:
        return sum([int(pi.value) for pi in self.part_inventory if pi.partID == part_id], ZERO)

    def get_incoming_inventory(self, part_id: str) -> Decimal:
        return ZERO
