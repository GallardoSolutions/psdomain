"""
Tests for product data converters (v100, v200).

Tests roundtrip conversion: JSON -> Pydantic -> Proto -> Pydantic
"""
from psdomain.model.product_data.v_1_0_0 import ProductResponseV100
from psdomain.model.product_data.v_2_0_0 import ProductResponseV200
from psdomain.converters.product import v100, v200


class TestProductV100Converter:
    """Tests for Product Data v1.0.0 converter."""

    def test_basic_product_response(self):
        """Test basic product response conversion."""
        json_data = {
            "Product": {
                "productId": "TEST-001",
                "productName": "Test Product",
                "description": ["A test product description"],
                "priceExpiresDate": None,
                "ProductMarketingPointArray": None,
                "ProductKeywordArray": None,
                "productBrand": "TestBrand",
                "export": True,
                "ProductCategoryArray": None,
                "RelatedProductArray": None,
                "ProductPartArray": {
                    "ProductPart": []
                },
                "lastChangeDate": None,
                "creationDate": None,
                "endDate": None,
                "effectiveDate": None,
                "isCaution": False,
                "cautionComment": None,
                "isCloseout": False,
                "lineName": None,
                "primaryImageURL": "https://example.com/image.jpg",
                "complianceInfoAvailable": False,
                "unspscCommodityCode": None,
                "imprintSize": None,
                "defaultSetUpCharge": None,
                "defaultRunCharge": None,
            },
            "ErrorMessage": None
        }

        pydantic_response = ProductResponseV100.model_validate(json_data)
        proto_response = v100.to_proto(pydantic_response)

        # Verify proto
        assert proto_response.product.product_id == "TEST-001"
        assert proto_response.product.product_name == "Test Product"
        assert proto_response.product.product_brand == "TestBrand"
        assert proto_response.product.export is True

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert roundtrip.Product.productId == "TEST-001"
        assert roundtrip.Product.productName == "Test Product"

    def test_product_with_parts(self):
        """Test product with parts array."""
        json_data = {
            "Product": {
                "productId": "PART-001",
                "productName": "Product with Parts",
                "description": None,
                "priceExpiresDate": None,
                "ProductMarketingPointArray": None,
                "ProductKeywordArray": None,
                "productBrand": None,
                "export": True,
                "ProductCategoryArray": None,
                "RelatedProductArray": None,
                "ProductPartArray": {
                    "ProductPart": [
                        {
                            "partId": "PART-A",
                            "description": ["Part A Description"],
                            "countryOfOrigin": "USA",
                            "ColorArray": {
                                "Color": [
                                    {
                                        "colorName": "Red",
                                        "hex": "FF0000",
                                        "approximatePms": None,
                                        "standardColorName": None
                                    }
                                ]
                            },
                            "primaryMaterial": None,
                            "SpecificationArray": None,
                            "shape": "Round",
                            "ApparelSize": None,
                            "Dimension": None,
                            "leadTime": 5,
                            "unspsc": None,
                            "gtin": None,
                            "isRushService": False,
                            "ProductPackagingArray": None,
                            "ShippingPackageArray": None,
                            "endDate": None,
                            "effectiveDate": None,
                            "isCloseout": False,
                            "isCaution": False,
                            "cautionComment": None,
                            "nmfcCode": None,
                            "nmfcDescription": None,
                            "nmfcNumber": None,
                            "isOnDemand": False,
                            "isHazmat": False,
                        }
                    ]
                },
                "lastChangeDate": None,
                "creationDate": None,
                "endDate": None,
                "effectiveDate": None,
                "isCaution": False,
                "cautionComment": None,
                "isCloseout": False,
                "lineName": None,
                "primaryImageURL": None,
                "complianceInfoAvailable": False,
                "unspscCommodityCode": None,
                "imprintSize": None,
                "defaultSetUpCharge": None,
                "defaultRunCharge": None,
            },
            "ErrorMessage": None
        }

        pydantic_response = ProductResponseV100.model_validate(json_data)
        proto_response = v100.to_proto(pydantic_response)

        # Verify proto parts
        assert len(proto_response.product.parts) == 1
        part = proto_response.product.parts[0]
        assert part.part_id == "PART-A"
        assert part.lead_time == 5
        assert len(part.colors) == 1
        assert part.colors[0].color_name == "Red"

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert len(roundtrip.Product.ProductPartArray.ProductPart) == 1
        assert roundtrip.Product.ProductPartArray.ProductPart[0].partId == "PART-A"

    def test_product_with_categories_and_keywords(self):
        """Test product with categories and keywords."""
        json_data = {
            "Product": {
                "productId": "CAT-001",
                "productName": "Categorized Product",
                "description": None,
                "priceExpiresDate": None,
                "ProductMarketingPointArray": {
                    "ProductMarketingPoint": [
                        {"pointType": "Feature", "pointCopy": "Amazing feature"}
                    ]
                },
                "ProductKeywordArray": {
                    "ProductKeyword": [
                        {"keyword": "promotional"},
                        {"keyword": "gift"}
                    ]
                },
                "productBrand": None,
                "export": True,
                "ProductCategoryArray": {
                    "ProductCategory": [
                        {"category": "Apparel", "subCategory": "T-Shirts"}
                    ]
                },
                "RelatedProductArray": None,
                "ProductPartArray": {"ProductPart": []},
                "lastChangeDate": None,
                "creationDate": None,
                "endDate": None,
                "effectiveDate": None,
                "isCaution": False,
                "cautionComment": None,
                "isCloseout": False,
                "lineName": None,
                "primaryImageURL": None,
                "complianceInfoAvailable": False,
                "unspscCommodityCode": None,
                "imprintSize": None,
                "defaultSetUpCharge": None,
                "defaultRunCharge": None,
            },
            "ErrorMessage": None
        }

        pydantic_response = ProductResponseV100.model_validate(json_data)
        proto_response = v100.to_proto(pydantic_response)

        # Verify proto categories and keywords
        assert len(proto_response.product.categories) == 1
        assert proto_response.product.categories[0].category == "Apparel"
        assert len(proto_response.product.keywords) == 2
        assert proto_response.product.marketing_points[0].point_copy == "Amazing feature"

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert len(roundtrip.Product.ProductCategoryArray.ProductCategory) == 1
        assert len(roundtrip.Product.ProductKeywordArray.ProductKeyword) == 2


class TestProductV200Converter:
    """Tests for Product Data v2.0.0 converter."""

    def test_basic_product_response(self):
        """Test basic v2.0.0 product response conversion."""
        json_data = {
            "Product": {
                "productId": "V200-001",
                "productName": "V2 Product",
                "description": ["Version 2 product"],
                "priceExpiresDate": None,
                "ProductMarketingPointArray": None,
                "ProductKeywordArray": None,
                "productBrand": "V2Brand",
                "export": True,
                "ProductCategoryArray": None,
                "RelatedProductArray": None,
                "ProductPartArray": {"ProductPart": []},
                "lastChangeDate": None,
                "creationDate": None,
                "endDate": None,
                "effectiveDate": None,
                "isCaution": False,
                "cautionComment": None,
                "isCloseout": False,
                "lineName": None,
                "primaryImageURL": None,
                "complianceInfoAvailable": False,
                "unspscCommodityCode": None,
                "imprintSize": None,
                "defaultSetUpCharge": None,
                "defaultRunCharge": None,
                "LocationDecorationArray": None,
                "ProductPriceGroupArray": None,
                "FobPointArray": None,
            },
            "ServiceMessageArray": None
        }

        pydantic_response = ProductResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify proto
        assert proto_response.product.product_id == "V200-001"
        assert proto_response.product.product_name == "V2 Product"
        assert proto_response.product.product_brand == "V2Brand"

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        assert roundtrip.Product.productId == "V200-001"
        assert roundtrip.Product.productBrand == "V2Brand"

    def test_product_with_service_messages(self):
        """Test product response with service messages."""
        json_data = {
            "Product": None,
            "ServiceMessageArray": {
                "ServiceMessage": [
                    {"code": 404, "description": "Product not found", "severity": "Error"}
                ]
            }
        }

        pydantic_response = ProductResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify service messages
        assert len(proto_response.service_messages) == 1
        assert proto_response.service_messages[0].code == 404

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        assert roundtrip.Product is None
        assert roundtrip.ServiceMessageArray.ServiceMessage[0].code == 404

    def test_product_with_specifications(self):
        """Test product with specifications."""
        json_data = {
            "Product": {
                "productId": "SPEC-001",
                "productName": "Product with Specs",
                "description": None,
                "priceExpiresDate": None,
                "ProductMarketingPointArray": None,
                "ProductKeywordArray": None,
                "productBrand": None,
                "export": True,
                "ProductCategoryArray": None,
                "RelatedProductArray": None,
                "ProductPartArray": {
                    "ProductPart": [
                        {
                            "partId": "SPEC-PART",
                            "description": ["Spec part description"],
                            "countryOfOrigin": "China",
                            "ColorArray": None,
                            "primaryMaterial": "Cotton",
                            "SpecificationArray": {
                                "Specification": [
                                    {"specificationType": "Length", "SpecificationUom": "oz", "measurementValue": "5.5"}
                                ]
                            },
                            "shape": "Rectangle",
                            "ApparelSize": None,
                            "Dimension": {
                                "height": 10.0,
                                "width": 5.0,
                                "depth": 2.0,
                                "weight": 0.5,
                                "dimensionUom": "IN",
                                "weightUom": "LB"
                            },
                            "leadTime": None,
                            "unspsc": None,
                            "gtin": None,
                            "isRushService": False,
                            "ProductPackagingArray": None,
                            "ShippingPackageArray": None,
                            "endDate": None,
                            "effectiveDate": None,
                            "isCloseout": False,
                            "isCaution": False,
                            "cautionComment": None,
                            "nmfcCode": None,
                            "nmfcDescription": None,
                            "nmfcNumber": None,
                            "isOnDemand": False,
                            "isHazmat": False,
                        }
                    ]
                },
                "lastChangeDate": None,
                "creationDate": None,
                "endDate": None,
                "effectiveDate": None,
                "isCaution": False,
                "cautionComment": None,
                "isCloseout": False,
                "lineName": None,
                "primaryImageURL": None,
                "complianceInfoAvailable": False,
                "unspscCommodityCode": None,
                "imprintSize": None,
                "defaultSetUpCharge": None,
                "defaultRunCharge": None,
                "LocationDecorationArray": None,
                "ProductPriceGroupArray": None,
                "FobPointArray": None,
            },
            "ServiceMessageArray": None
        }

        pydantic_response = ProductResponseV200.model_validate(json_data)
        proto_response = v200.to_proto(pydantic_response)

        # Verify specs and dimensions
        part = proto_response.product.parts[0]
        assert len(part.specifications) == 1
        assert part.specifications[0].specification_type == "Length"
        assert part.primary_material == "Cotton"
        assert part.dimension.height == "10.0"

        # Roundtrip
        roundtrip = v200.from_proto(proto_response)
        rt_part = roundtrip.Product.ProductPartArray.ProductPart[0]
        assert rt_part.primaryMaterial == "Cotton"
        assert rt_part.Dimension.height == 10.0
