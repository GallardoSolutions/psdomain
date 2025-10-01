from decimal import Decimal

from psdomain.model.product_data.common import (
    ProductPriceGroup,
    ProductPriceArray,
    ProductPrice
)


class TestProductPriceGroup:
    def test_product_price_group_with_none_price_array(self):
        """Test that ProductPriceGroup can have None ProductPriceArray"""
        price_group = ProductPriceGroup(
            groupName="USD-List-Blank",
            currency="USD",
            description="Test description",
            ProductPriceArray=None
        )

        assert price_group.groupName == "USD-List-Blank"
        assert price_group.currency == "USD"
        assert price_group.description == "Test description"
        assert price_group.ProductPriceArray is None
        assert price_group.prices == []

    def test_product_price_group_with_price_array(self):
        """Test that ProductPriceGroup works with ProductPriceArray"""
        price_array = ProductPriceArray(
            ProductPrice=[
                ProductPrice(
                    quantityMin=1,
                    quantityMax=100,
                    price=Decimal("10.50"),
                    discountCode="C"
                ),
                ProductPrice(
                    quantityMin=101,
                    quantityMax=None,
                    price=Decimal("8.75"),
                    discountCode="D"
                )
            ]
        )

        price_group = ProductPriceGroup(
            groupName="USD-List-Decorated",
            currency="USD",
            description="Decorated prices",
            ProductPriceArray=price_array
        )

        assert price_group.groupName == "USD-List-Decorated"
        assert price_group.currency == "USD"
        assert price_group.description == "Decorated prices"
        assert price_group.ProductPriceArray is not None
        assert len(price_group.prices) == 2
        assert price_group.prices[0].price == Decimal("10.50")
        assert price_group.prices[1].price == Decimal("8.75")

    def test_product_price_group_without_price_array_field(self):
        """Test that ProductPriceGroup can be created without ProductPriceArray field"""
        price_group = ProductPriceGroup(
            groupName="CAD-List",
            currency="CAD",
            description=None
        )

        assert price_group.groupName == "CAD-List"
        assert price_group.currency == "CAD"
        assert price_group.description is None
        assert price_group.ProductPriceArray is None
        assert price_group.prices == []
