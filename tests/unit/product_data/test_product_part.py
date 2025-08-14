from psdomain.model.product_data.common import ProductPart, Color, ColorArray, PrimaryColor

default_values = dict(
    countryOfOrigin=None,
    primaryMaterial=None,
    SpecificationArray=None,
    shape=None,
    ApparelSize=None,
    Dimension=None,
    leadTime=None,
    unspsc=None,
    gtin=None,
    isRushService=None,
    endDate=None,
    effectiveDate=None,
    isCloseout=None,
    isCaution=None,
    cautionComment=None,
    nmfcCode=None,
    nmfcDescription=None,
    nmfcNumber=None,
    isOnDemand=None,
    isHazmat=None,
    ProductPackagingArray=None,
    ShippingPackageArray=None
)


class TestProductPartGetPrimaryColor:
    def test_get_primary_color_default_color_field(self):
        """Test get_primary_color when color_field is not passed (uses default 'colorName')"""
        # Test case 1: ProductPart with ColorArray
        color1 = Color(
            colorName="Red",
            hex="#FF0000",
            approximatePms="PMS 200",
            standardColorName="Crimson"
        )
        color2 = Color(
            colorName="Blue",
            hex="#0000FF",
            approximatePms="PMS 300",
            standardColorName="Navy"
        )
        color_array = ColorArray(Color=[color1, color2])

        product_part = ProductPart(
            partId="TEST-001",
            description=["Test product part"],
            ColorArray=color_array,
            primaryColor=None,
            **default_values
        )

        # Should return the colorName of the first color in ColorArray
        assert product_part.get_primary_color() == "Red"

        # Test case 2: ProductPart with primaryColor instead of ColorArray
        primary_color = PrimaryColor(
            Color=Color(
                colorName="Green",
                hex="#00FF00",
                approximatePms="PMS 400",
                standardColorName="Forest"
            )
        )

        product_part2 = ProductPart(
            partId="TEST-002",
            description=["Test product part 2"],
            primaryColor=primary_color,
            ColorArray=None,
            **default_values
        )

        # Should return the colorName from primaryColor
        assert product_part2.get_primary_color() == "Green"

        # Test case 3: ProductPart with no color information
        product_part3 = ProductPart(
            partId="TEST-003",
            description=["Test product part 3"],
            primaryColor=None,
            ColorArray=None,
            **default_values
        )

        # Should return empty string when no color is available
        assert product_part3.get_primary_color() == ""

    def test_get_primary_color_with_standard_color_name(self):
        """Test get_primary_color when color_field = 'standardColorName'"""
        # Test case 1: ProductPart with ColorArray
        color1 = Color(
            colorName="Red",
            hex="#FF0000",
            approximatePms="PMS 200",
            standardColorName="Crimson"
        )
        color2 = Color(
            colorName="Blue",
            hex="#0000FF",
            approximatePms="PMS 300",
            standardColorName="Navy"
        )
        color_array = ColorArray(Color=[color1, color2])

        product_part = ProductPart(
            partId="TEST-004",
            description=["Test product part"],
            ColorArray=color_array,
            **default_values
        )

        # Should return the standardColorName of the first color in ColorArray
        assert product_part.get_primary_color(color_field='standardColorName') == "Crimson"

        # Test case 2: ProductPart with primaryColor instead of ColorArray
        primary_color = PrimaryColor(
            Color=Color(
                colorName="Green",
                hex="#00FF00",
                approximatePms="PMS 400",
                standardColorName="Forest"
            )
        )

        product_part2 = ProductPart(
            partId="TEST-005",
            description=["Test product part 2"],
            primaryColor=primary_color,
            ColorArray=None,
            **default_values
        )

        # Should return the standardColorName from primaryColor
        assert product_part2.get_primary_color(color_field='standardColorName') == "Forest"

        # Test case 3: ProductPart with no color information
        product_part3 = ProductPart(
            partId="TEST-006",
            description=["Test product part 3"],
            ColorArray=None,
            **default_values
        )

        # Should return empty string when no color is available
        assert product_part3.get_primary_color(color_field='standardColorName') == ""

        # Test case 4: Color with None standardColorName
        color_with_none = Color(
            colorName="Purple",
            hex="#800080",
            approximatePms="PMS 500",
            standardColorName=None
        )
        color_array_with_none = ColorArray(Color=[color_with_none])

        product_part4 = ProductPart(
            partId="TEST-007",
            description=["Test product part 4"],
            ColorArray=color_array_with_none,
            **default_values
        )

        # Should return None when standardColorName is None
        assert product_part4.get_primary_color(color_field='standardColorName') is None
