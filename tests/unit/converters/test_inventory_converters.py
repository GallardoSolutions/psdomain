"""
Tests for inventory converters (v121, v200).

Tests roundtrip conversion: JSON -> Pydantic -> Proto -> Pydantic
"""
import pytest

from psdomain.model.inventory.v_2_0_0 import (
    InventoryLevelsResponseV200,
    FilterValuesResponseV200,
)
from psdomain.model.inventory.v_1_2_1 import InventoryLevelsResponseV121
from psdomain.converters.inventory import v200, v121


class TestInventoryV200Converter:
    """Tests for Inventory v2.0.0 converter."""

    def test_pcna_1080_30_empty_parts(self):
        """Test converting PCNA-1080-30 response with empty parts array."""
        # JSON response from PCNA
        json_data = {
            "ServiceMessageArray": None,
            "Inventory": {
                "productId": "1080-30",
                "PartInventoryArray": {
                    "PartInventory": []
                }
            }
        }

        # Parse JSON to Pydantic
        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)

        # Verify pydantic parsing
        assert pydantic_response.Inventory is not None
        assert pydantic_response.Inventory.productId == "1080-30"
        assert pydantic_response.Inventory.PartInventoryArray is not None
        assert pydantic_response.Inventory.PartInventoryArray.PartInventory == []
        assert pydantic_response.ServiceMessageArray is None

        # Convert Pydantic -> Proto
        proto_response = v200.to_proto(pydantic_response)

        # Verify proto conversion
        assert proto_response.inventory.product_id == "1080-30"
        assert len(proto_response.inventory.part_inventory) == 0
        assert len(proto_response.service_messages) == 0

        # Convert Proto -> Pydantic
        roundtrip_response = v200.from_proto(proto_response)

        # Verify roundtrip
        assert roundtrip_response.Inventory is not None
        assert roundtrip_response.Inventory.productId == "1080-30"
        assert roundtrip_response.Inventory.PartInventoryArray is not None
        assert roundtrip_response.Inventory.PartInventoryArray.PartInventory == []

    def test_inventory_with_parts_and_quantity(self):
        """Test inventory response with parts and quantity available."""
        json_data = {
            "ServiceMessageArray": None,
            "Inventory": {
                "productId": "TEST-001",
                "PartInventoryArray": {
                    "PartInventory": [
                        {
                            "partId": "PART-A",
                            "mainPart": True,
                            "partColor": "Red",
                            "labelSize": "M",
                            "partDescription": "Test Part A",
                            "quantityAvailable": {
                                "Quantity": {
                                    "value": 100,
                                    "uom": "EA"
                                }
                            },
                            "manufacturedItem": False,
                            "buyToOrder": False,
                            "replenishmentLeadTime": 5,
                            "attributeSelection": None,
                            "InventoryLocationArray": None
                        }
                    ]
                }
            }
        }

        # Parse JSON to Pydantic
        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)

        # Convert Pydantic -> Proto
        proto_response = v200.to_proto(pydantic_response)

        # Verify proto
        assert proto_response.inventory.product_id == "TEST-001"
        assert len(proto_response.inventory.part_inventory) == 1
        part = proto_response.inventory.part_inventory[0]
        assert part.part_id == "PART-A"
        assert part.main_part is True
        assert part.part_color == "Red"
        assert part.label_size == "M"
        assert part.quantity_available.value == 100
        assert part.quantity_available.uom == "EA"

        # Convert Proto -> Pydantic
        roundtrip_response = v200.from_proto(proto_response)

        # Verify roundtrip
        assert roundtrip_response.Inventory.productId == "TEST-001"
        parts = roundtrip_response.Inventory.PartInventoryArray.PartInventory
        assert len(parts) == 1
        assert parts[0].partId == "PART-A"
        assert parts[0].mainPart is True
        assert parts[0].quantityAvailable.Quantity.value == 100

    def test_inventory_with_locations(self):
        """Test inventory response with inventory locations."""
        json_data = {
            "ServiceMessageArray": None,
            "Inventory": {
                "productId": "LOC-001",
                "PartInventoryArray": {
                    "PartInventory": [
                        {
                            "partId": "PART-LOC",
                            "mainPart": True,
                            "partColor": None,
                            "labelSize": None,
                            "partDescription": "Part with locations",
                            "quantityAvailable": {
                                "Quantity": {"value": 500, "uom": "EA"}
                            },
                            "manufacturedItem": False,
                            "buyToOrder": False,
                            "replenishmentLeadTime": None,
                            "attributeSelection": None,
                            "InventoryLocationArray": {
                                "InventoryLocation": [
                                    {
                                        "inventoryLocationId": "WH-001",
                                        "inventoryLocationName": "Main Warehouse",
                                        "postalCode": "90210",
                                        "country": "US",
                                        "inventoryLocationQuantity": {
                                            "Quantity": {"value": 300, "uom": "EA"}
                                        },
                                        "FutureAvailabilityArray": None
                                    },
                                    {
                                        "inventoryLocationId": "WH-002",
                                        "inventoryLocationName": "East Warehouse",
                                        "postalCode": "10001",
                                        "country": "US",
                                        "inventoryLocationQuantity": {
                                            "Quantity": {"value": 200, "uom": "EA"}
                                        },
                                        "FutureAvailabilityArray": None
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify proto locations
        assert len(proto_response.inventory.part_inventory) == 1
        part = proto_response.inventory.part_inventory[0]
        assert len(part.inventory_locations) == 2
        assert part.inventory_locations[0].inventory_location_id == "WH-001"
        assert part.inventory_locations[0].inventory_location_quantity.value == 300
        assert part.inventory_locations[1].inventory_location_id == "WH-002"

        # Roundtrip
        roundtrip_response = v200.from_proto(proto_response)
        roundtrip_part = roundtrip_response.Inventory.PartInventoryArray.PartInventory[0]
        locs = roundtrip_part.InventoryLocationArray.InventoryLocation
        assert len(locs) == 2
        assert locs[0].inventoryLocationId == "WH-001"
        assert locs[0].inventoryLocationQuantity.Quantity.value == 300

    def test_inventory_with_future_availability(self):
        """Test inventory with future availability dates."""
        json_data = {
            "ServiceMessageArray": None,
            "Inventory": {
                "productId": "FUT-001",
                "PartInventoryArray": {
                    "PartInventory": [
                        {
                            "partId": "PART-FUT",
                            "mainPart": True,
                            "partColor": None,
                            "labelSize": None,
                            "partDescription": None,
                            "quantityAvailable": {
                                "Quantity": {"value": 50, "uom": "EA"}
                            },
                            "manufacturedItem": False,
                            "buyToOrder": False,
                            "replenishmentLeadTime": None,
                            "attributeSelection": None,
                            "InventoryLocationArray": {
                                "InventoryLocation": [
                                    {
                                        "inventoryLocationId": "WH-001",
                                        "inventoryLocationName": None,
                                        "postalCode": None,
                                        "country": None,
                                        "inventoryLocationQuantity": {
                                            "Quantity": {"value": 50, "uom": "EA"}
                                        },
                                        "FutureAvailabilityArray": {
                                            "FutureAvailability": [
                                                {
                                                    "availableOn": "2025-02-01T00:00:00",
                                                    "Quantity": {"value": 100, "uom": "EA"}
                                                },
                                                {
                                                    "availableOn": "2025-03-01T00:00:00",
                                                    "Quantity": {"value": 200, "uom": "EA"}
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
        }

        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify future availability in proto (uses quantity_value and quantity_uom fields)
        loc = proto_response.inventory.part_inventory[0].inventory_locations[0]
        assert len(loc.future_availability) == 2
        assert loc.future_availability[0].quantity_value == 100
        assert loc.future_availability[1].quantity_value == 200

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        rt_loc = roundtrip.Inventory.PartInventoryArray.PartInventory[0].InventoryLocationArray.InventoryLocation[0]
        assert len(rt_loc.FutureAvailabilityArray.FutureAvailability) == 2

    def test_inventory_with_service_messages(self):
        """Test inventory response with service messages."""
        json_data = {
            "ServiceMessageArray": {
                "ServiceMessage": [
                    {
                        "code": 100,
                        "description": "Product found",
                        "severity": "Information"
                    },
                    {
                        "code": 200,
                        "description": "Limited stock",
                        "severity": "Warning"
                    }
                ]
            },
            "Inventory": {
                "productId": "MSG-001",
                "PartInventoryArray": {
                    "PartInventory": []
                }
            }
        }

        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify service messages in proto
        assert len(proto_response.service_messages) == 2
        assert proto_response.service_messages[0].code == 100
        assert proto_response.service_messages[0].description == "Product found"
        assert proto_response.service_messages[1].code == 200

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        assert roundtrip.ServiceMessageArray is not None
        msgs = roundtrip.ServiceMessageArray.ServiceMessage
        assert len(msgs) == 2
        assert msgs[0].code == 100
        assert msgs[1].description == "Limited stock"

    def test_filter_values_response(self):
        """Test filter values response conversion."""
        json_data = {
            "ServiceMessageArray": None,
            "FilterValues": {
                "productId": "FILTER-001",
                "Filter": {
                    "partIdArray": {"partId": ["PART-A", "PART-B"]},
                    "LabelSizeArray": {"labelSize": ["S", "M", "L"]},
                    "PartColorArray": {"partColor": ["Red", "Blue"]}
                }
            }
        }

        pydantic_response = FilterValuesResponseV200.model_validate(json_data)
        proto_response = v200.filter_values_response_to_proto(pydantic_response)

        # Verify proto
        assert proto_response.filter_values.product_id == "FILTER-001"
        assert "PART-A" in proto_response.filter_values.part_ids
        assert "PART-B" in proto_response.filter_values.part_ids
        assert "M" in proto_response.filter_values.label_sizes
        assert "Red" in proto_response.filter_values.part_colors

        # Roundtrip
        roundtrip = v200.filter_values_response_from_proto(proto_response)
        assert roundtrip.FilterValues.productId == "FILTER-001"

    def test_null_inventory(self):
        """Test response with null inventory."""
        json_data = {
            "ServiceMessageArray": {
                "ServiceMessage": [
                    {"code": 404, "description": "Product not found", "severity": "Error"}
                ]
            },
            "Inventory": None
        }

        pydantic_response = InventoryLevelsResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Should still have service messages
        assert len(proto_response.service_messages) == 1
        assert proto_response.service_messages[0].code == 404

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        assert roundtrip.Inventory is None
        assert roundtrip.ServiceMessageArray.ServiceMessage[0].code == 404


class TestInventoryV121Converter:
    """Tests for Inventory v1.2.1 converter."""

    def test_basic_inventory_response(self):
        """Test basic v1.2.1 inventory response."""
        # v1.2.1 uses partID (uppercase D), productID (uppercase D), and quantityAvailable is a string
        json_data = {
            "productID": "V121-001",
            "ProductVariationInventoryArray": {
                "ProductVariationInventory": [
                    {
                        "partID": "PART-121",
                        "partDescription": "Test Part",
                        "partBrand": "TestBrand",
                        "priceVariance": None,
                        "quantityAvailable": "100",
                        "AttributeFlexArray": {
                            "AttributeFlex": [
                                {"id": "SIZE", "name": "Size", "value": "Large"}
                            ]
                        },
                        "customProductMessage": None,
                        "entryType": None,
                        "validTimestamp": None
                    }
                ]
            },
            "ProductCompanionInventoryArray": None,
            "errorMessage": None
        }

        pydantic_response = InventoryLevelsResponseV121.model_validate(json_data)
        proto_response = v121.to_proto(pydantic_response)

        # Verify proto - v121 returns GetInventoryLevelsResponseV121 with nested inventory
        assert proto_response.inventory.product_id == "V121-001"
        assert len(proto_response.inventory.product_variations) == 1
        var = proto_response.inventory.product_variations[0]
        assert var.part_id == "PART-121"
        assert var.quantity_available == 100
        assert len(var.flex_attributes) == 1
        assert var.flex_attributes[0].id == "SIZE"

        # Roundtrip
        roundtrip = v121.from_proto(proto_response)
        assert roundtrip.productID == "V121-001"
        parts = roundtrip.ProductVariationInventoryArray.ProductVariationInventory
        assert len(parts) == 1
        assert parts[0].partID == "PART-121"
        assert parts[0].quantityAvailable == "100"

    @pytest.mark.skip(
        reason="InventoryLevelsResponseV121 pydantic model has constraint on ProductCompanionInventoryArray"
    )
    def test_v121_with_companion_inventory(self):
        """Test v1.2.1 with companion inventory."""
        json_data = {
            "productID": "COMP-001",
            "ProductVariationInventoryArray": {
                "ProductVariationInventory": [
                    {
                        "partID": "MAIN-PART",
                        "partDescription": "Main Product",
                        "partBrand": None,
                        "priceVariance": None,
                        "quantityAvailable": "50",
                        "AttributeFlexArray": None,
                        "customProductMessage": None,
                        "entryType": None,
                        "validTimestamp": None
                    }
                ]
            },
            "ProductCompanionInventoryArray": {
                "ProductCompanionInventory": [
                    {
                        "partID": "COMP-PART-A",
                        "partDescription": "Companion A",
                        "partBrand": None,
                        "price": None,
                        "quantityAvailable": "25",
                        "AttributeFlexArray": None,
                        "customProductMessage": None,
                        "entryType": None,
                        "validTimestamp": None
                    }
                ]
            },
            "errorMessage": None
        }

        pydantic_response = InventoryLevelsResponseV121.model_validate(json_data)
        proto_response = v121.to_proto(pydantic_response)

        # Verify proto
        assert len(proto_response.inventory.product_companions) == 1
        comp = proto_response.inventory.product_companions[0]
        assert comp.part_id == "COMP-PART-A"
        assert comp.quantity_available == 25

        # Roundtrip
        roundtrip = v121.from_proto(proto_response)
        comp_array = roundtrip.ProductCompanionInventoryArray.ProductCompanionInventory
        assert len(comp_array) == 1
        assert comp_array[0].partID == "COMP-PART-A"

    def test_v121_empty_arrays(self):
        """Test v1.2.1 with empty arrays."""
        json_data = {
            "productID": "EMPTY-121",
            "ProductVariationInventoryArray": {
                "ProductVariationInventory": []
            },
            "ProductCompanionInventoryArray": None,
            "errorMessage": None
        }

        pydantic_response = InventoryLevelsResponseV121.model_validate(json_data)
        proto_response = v121.to_proto(pydantic_response)

        assert proto_response.inventory.product_id == "EMPTY-121"
        assert len(proto_response.inventory.product_variations) == 0

        roundtrip = v121.from_proto(proto_response)
        assert roundtrip.productID == "EMPTY-121"

    def test_v121_with_attribute_flex(self):
        """Test v1.2.1 with multiple attribute flex values."""
        json_data = {
            "productID": "FLEX-001",
            "ProductVariationInventoryArray": {
                "ProductVariationInventory": [
                    {
                        "partID": "PART-FLEX",
                        "partDescription": "Part with flex attributes",
                        "partBrand": None,
                        "priceVariance": None,
                        "quantityAvailable": "75",
                        "attributeColor": "Blue",
                        "attributeSize": "Large",
                        "AttributeFlexArray": {
                            "AttributeFlex": [
                                {"id": "MATERIAL", "name": "Material", "value": "Cotton"},
                                {"id": "WEIGHT", "name": "Weight", "value": "200g"}
                            ]
                        },
                        "customProductMessage": "Custom message",
                        "entryType": "Standard",
                        "validTimestamp": None
                    }
                ]
            },
            "ProductCompanionInventoryArray": None,
            "errorMessage": None
        }

        pydantic_response = InventoryLevelsResponseV121.model_validate(json_data)
        proto_response = v121.to_proto(pydantic_response)

        # Verify proto - uses flex_attributes in proto
        var = proto_response.inventory.product_variations[0]
        assert len(var.flex_attributes) == 2
        assert var.flex_attributes[0].id == "MATERIAL"
        assert var.flex_attributes[0].value == "Cotton"
        assert var.flex_attributes[1].id == "WEIGHT"
        assert var.attribute_color == "Blue"
        assert var.attribute_size == "Large"
        assert var.custom_product_message == "Custom message"

        # Roundtrip
        roundtrip = v121.from_proto(proto_response)
        rt_part = roundtrip.ProductVariationInventoryArray.ProductVariationInventory[0]
        assert len(rt_part.AttributeFlexArray.AttributeFlex) == 2
        assert rt_part.attributeColor == "Blue"
        assert rt_part.attributeSize == "Large"
