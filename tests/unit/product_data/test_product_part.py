from psdomain.model.product_data.common import (
    ProductPart, Color, ColorArray, PrimaryColor,
    ProductPartArray, ApparelSize, ApparelStyle
)

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


class TestProductPartArrayGetNumberOfColors:
    color_red = Color(colorName="Red", hex="#FF0000", approximatePms="PMS 200", standardColorName="Crimson")
    color_blue = Color(colorName="Blue", hex="#0000FF", approximatePms="PMS 300", standardColorName="Navy")
    color_green = Color(colorName="Green", hex="#00FF00", approximatePms="PMS 400", standardColorName="Forest")

    def test_get_number_of_colors_empty_array(self):
        """Test get_number_of_colors with empty ProductPart array"""
        product_part_array = ProductPartArray(ProductPart=[])
        assert product_part_array.get_number_of_colors() == 0

    def test_get_number_of_colors_single_color(self):
        """Test get_number_of_colors with single color across multiple parts"""

        color_array = ColorArray(Color=[self.color_red])

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ColorArray=color_array,
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ColorArray=color_array,
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_colors() == 1

    def test_get_number_of_colors_multiple_unique_colors(self):
        """Test get_number_of_colors with multiple unique colors"""

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ColorArray=ColorArray(Color=[self.color_red]),
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ColorArray=ColorArray(Color=[self.color_blue]),
            **default_values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ColorArray=ColorArray(Color=[self.color_green]),
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        assert product_part_array.get_number_of_colors() == 3

    def test_get_number_of_colors_duplicate_colors(self):
        """Test get_number_of_colors with duplicate colors (should count unique only)"""

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ColorArray=ColorArray(Color=[self.color_red]),
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ColorArray=ColorArray(Color=[self.color_blue]),
            **default_values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ColorArray=ColorArray(Color=[self.color_red]),  # Duplicate red
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        assert product_part_array.get_number_of_colors() == 2

    def test_get_number_of_colors_with_primary_color(self):
        """Test get_number_of_colors with parts using primaryColor instead of ColorArray"""

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            primaryColor=PrimaryColor(Color=self.color_red),
            ColorArray=None,
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            primaryColor=PrimaryColor(Color=self.color_blue),
            ColorArray=None,
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_colors() == 2

    def test_get_number_of_colors_mixed_color_sources(self):
        """Test get_number_of_colors with parts using both ColorArray and primaryColor"""

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ColorArray=ColorArray(Color=[self.color_red]),
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            primaryColor=PrimaryColor(Color=self.color_blue),
            ColorArray=None,
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_colors() == 2

    def test_get_number_of_colors_with_no_colors(self):
        """Test get_number_of_colors with parts that have no color information"""
        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ColorArray=None,
            primaryColor=None,
            **default_values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ColorArray=None,
            primaryColor=None,
            **default_values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        # Parts with no colors will contribute empty strings, which form a single unique value
        assert product_part_array.get_number_of_colors() == 1


class TestProductPartArrayGetNumberOfSizes:
    apparel_size_s = ApparelSize(
        apparelStyle=ApparelStyle.Mens,
        labelSize="S",
        customSize=None
    )
    apparel_size_m = ApparelSize(
        apparelStyle=ApparelStyle.Mens,
        labelSize="M",
        customSize=None
    )
    apparel_size_l = ApparelSize(
        apparelStyle=ApparelStyle.Mens,
        labelSize="L",
        customSize=None
    )

    @staticmethod
    def gen_default_values(apparel_size=None, include_size=True):
        values = default_values.copy()
        if include_size:
            values['ApparelSize'] = apparel_size
        else:
            values.pop('ApparelSize', None)
        values['ColorArray'] = None
        return values

    def test_get_number_of_sizes_empty_array(self):
        """Test get_number_of_sizes with empty ProductPart array"""
        product_part_array = ProductPartArray(ProductPart=[])
        assert product_part_array.get_number_of_sizes() == 0

    def test_get_number_of_sizes_no_apparel_sizes(self):
        """Test get_number_of_sizes with parts that have no ApparelSize"""
        values = self.gen_default_values()
        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_sizes() == 0

    def test_get_number_of_sizes_single_size(self):
        """Test get_number_of_sizes with single size across multiple parts"""
        values = self.gen_default_values(self.apparel_size_m)
        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_sizes() == 1

    def test_get_number_of_sizes_multiple_unique_sizes(self):
        """Test get_number_of_sizes with multiple unique sizes"""
        values = self.gen_default_values(include_size=False)
        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=self.apparel_size_s,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=self.apparel_size_m,
            **values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ApparelSize=self.apparel_size_l,
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        assert product_part_array.get_number_of_sizes() == 3

    def test_get_number_of_sizes_duplicate_sizes(self):
        """Test get_number_of_sizes with duplicate sizes (should count unique only)"""
        values = self.gen_default_values(include_size=False)
        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=self.apparel_size_m,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=self.apparel_size_l,
            **values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ApparelSize=self.apparel_size_m,  # Duplicate M
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        assert product_part_array.get_number_of_sizes() == 2

    def test_get_number_of_sizes_with_custom_sizes(self):
        """Test get_number_of_sizes with custom sizes"""
        values = self.gen_default_values(include_size=False)
        apparel_size_custom1 = ApparelSize(
            apparelStyle=ApparelStyle.Mens,
            labelSize="CUSTOM",
            customSize="42R"
        )
        apparel_size_custom2 = ApparelSize(
            apparelStyle=ApparelStyle.Mens,
            labelSize="CUSTOM",
            customSize="44L"
        )

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=apparel_size_custom1,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=apparel_size_custom2,
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        # Should count unique custom sizes
        assert product_part_array.get_number_of_sizes() == 2

    def test_get_number_of_sizes_mixed_regular_and_custom(self):
        """Test get_number_of_sizes with mix of regular and custom sizes"""
        values = self.gen_default_values(include_size=False)
        apparel_size_custom = ApparelSize(
            apparelStyle=ApparelStyle.Mens,
            labelSize="CUSTOM",
            customSize="42R"
        )

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=self.apparel_size_m,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=apparel_size_custom,
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2])
        assert product_part_array.get_number_of_sizes() == 2

    def test_get_number_of_sizes_empty_label_size(self):
        """Test get_number_of_sizes with empty label sizes"""
        values = self.gen_default_values(include_size=False)
        apparel_size_empty = ApparelSize(
            apparelStyle=ApparelStyle.Mens,
            labelSize="",
            customSize=None
        )

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=apparel_size_empty,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=self.apparel_size_m,
            **values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ApparelSize=apparel_size_empty,
            **values
        )
        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        # Empty sizes should be filtered out
        assert product_part_array.get_number_of_sizes() == 2

    def test_get_number_of_sizes_mixed_with_and_without_sizes(self):
        """Test get_number_of_sizes with mix of parts with and without sizes"""
        values = self.gen_default_values(include_size=False)

        part1 = ProductPart(
            partId="TEST-001",
            description=["Test part 1"],
            ApparelSize=self.apparel_size_m,
            **values
        )
        part2 = ProductPart(
            partId="TEST-002",
            description=["Test part 2"],
            ApparelSize=None,  # No size
            **values
        )
        part3 = ProductPart(
            partId="TEST-003",
            description=["Test part 3"],
            ApparelSize=self.apparel_size_l,
            **values
        )

        product_part_array = ProductPartArray(ProductPart=[part1, part2, part3])
        assert product_part_array.get_number_of_sizes() == 2
