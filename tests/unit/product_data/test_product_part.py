import pytest

from psdomain.model.product_data.common import (
    ProductPart, Color, ColorArray, PrimaryColor,
    ProductPartArray, ApparelSize, ApparelStyle, canonical_size,
    STANDARD_SIZES, SIZE_ALIASES, SIZES, sort_sizes,
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


def gen_sized_part(part_id, label_size, custom_size, color="SCARLET"):
    """A ProductPart with one color and the given ApparelSize."""
    values = default_values.copy()
    values["ApparelSize"] = ApparelSize(
        apparelStyle=ApparelStyle.Boys, labelSize=label_size, customSize=custom_size)
    values["ColorArray"] = ColorArray(Color=[Color(
        colorName=color, hex="ed2c2f", approximatePms=None, standardColorName="Red")])
    return ProductPart(partId=part_id, description=[color], **values)


# Real feed values that must never be mistaken for a standard size.
FREE_TEXT_SIZES = (
    "S/M", "XS/S", "L/XL", "M/L", "XXS/XS",   # Champro / Wholesale Printables combos
    "LXL",                                   # A4 combined L/XL (under CUSTOM)
    "LT", "XLT", "2XLT", "ST", "MT",         # tall sizes: distinct, never fold to L/XL
    "42R", "44L",                            # suit sizes
    "32", "7", "10",                         # numeric sizes
    "NA", "CUSTOM", "-",                     # fillers
    "Adult", "YOUTH", "Youth 1-1/4\"", "9\"", "12 oz.",
)


class TestCanonicalSize:
    """canonical_size(): spec token for a size spelling, None for anything else."""

    @pytest.mark.parametrize("token", sorted(STANDARD_SIZES))
    def test_every_standard_token_passes_through(self, token):
        assert canonical_size(token) == token

    def test_case_whitespace_and_hyphen_are_ignored(self):
        assert canonical_size(" xs ") == "XS"
        assert canonical_size("2-XL") == "2XL"
        assert canonical_size("2xl") == "2XL"
        assert canonical_size("x-large") is None  # not an alias we know

    @pytest.mark.parametrize("alias, token", sorted(SIZE_ALIASES.items()))
    def test_every_alias_resolves_to_a_standard_token(self, alias, token):
        assert token in STANDARD_SIZES, f"alias {alias!r} targets non-standard {token!r}"
        assert canonical_size(alias) == token
        assert canonical_size(alias.lower()) == token

    def test_real_feed_aliases(self):
        # A4/Boxercraft "XXS", Colosseum "XXL"/"Xxl", Royal Apparel "2X",
        # Pennant "SM/MD/LG", Pearsox "MEDIUM", Champro "ONE SIZE"/"OSFM".
        assert canonical_size("XXS") == "2XS"
        assert canonical_size("XXL") == "2XL"
        assert canonical_size("Xxl") == "2XL"
        assert canonical_size("2X") == "2XL"
        assert canonical_size("SM") == "S"
        assert canonical_size("MEDIUM") == "M"
        assert canonical_size("ONE SIZE") == "OSFA"
        assert canonical_size("OSFM") == "OSFA"

    @pytest.mark.parametrize("value", FREE_TEXT_SIZES)
    def test_free_text_is_not_a_size(self, value):
        assert canonical_size(value) is None

    def test_empty_is_none(self):
        assert canonical_size("") is None
        assert canonical_size(None) is None
        assert canonical_size("   ") is None

    def test_standard_sizes_are_a_subset_of_the_sort_vocabulary(self):
        # sort_sizes() ranks by SIZES; every token get_size() can emit must sort.
        assert STANDARD_SIZES <= set(SIZES)


class TestProductPartGetSizeSpecPath:
    """labelSize CUSTOM: customSize is the size, returned verbatim (never canonicalized)."""

    def test_free_text_verbatim(self):
        assert gen_sized_part("P1", "CUSTOM", "42R").get_size() == "42R"
        assert gen_sized_part("P2", "CUSTOM", "M/XL").get_size() == "M/XL"

    def test_standard_token_verbatim(self):
        # Champro files S/M/L/XL/2XL under CUSTOM: 22k parts that must not move.
        assert gen_sized_part("P1", "CUSTOM", "2XL").get_size() == "2XL"
        assert gen_sized_part("P2", "CUSTOM", "M").get_size() == "M"

    def test_alias_is_not_canonicalized(self):
        # The CUSTOM path is deliberately left alone: no drift for existing stores.
        assert gen_sized_part("P1", "CUSTOM", "XXL").get_size() == "XXL"
        assert gen_sized_part("P2", "CUSTOM", "XXS").get_size() == "XXS"

    def test_whitespace_is_stripped(self):
        assert gen_sized_part("P1", "CUSTOM", "  42R  ").get_size() == "42R"
        assert gen_sized_part("P2", " CUSTOM ", "42R").get_size() == "42R"

    def test_lowercase_custom_label(self):
        assert gen_sized_part("P1", "custom", "42R").get_size() == "42R"

    def test_missing_custom_size_is_empty_string_not_none(self):
        # Champro CPN3: CUSTOM with no customSize. Was None; callers do `or ''`.
        assert gen_sized_part("P1", "CUSTOM", None).get_size() == ""
        assert gen_sized_part("P2", "CUSTOM", "").get_size() == ""
        assert gen_sized_part("P3", "CUSTOM", "  ").get_size() == ""


class TestProductPartGetSizePlainLabel:
    """labelSize present, customSize empty: the label is returned as sent."""

    def test_standard_label(self):
        assert gen_sized_part("P1", "XS", None).get_size() == "XS"
        assert gen_sized_part("P2", "2XL", "").get_size() == "2XL"

    def test_label_whitespace_is_stripped(self):
        assert gen_sized_part("P1", " XS ", None).get_size() == "XS"

    def test_off_spec_label_verbatim(self):
        # SanMar Canada sends "L/XL" as a labelSize.
        assert gen_sized_part("P1", "L/XL", None).get_size() == "L/XL"

    def test_label_case_is_never_rewritten(self):
        # We canonicalize customSize only; a store's existing label never changes.
        assert gen_sized_part("P1", "xs", None).get_size() == "xs"
        assert gen_sized_part("P2", "Medium", None).get_size() == "Medium"

    def test_no_apparel_size(self):
        values = default_values.copy()
        values["ColorArray"] = None
        assert ProductPart(partId="P1", description=["x"], **values).get_size() == ""

    def test_showdown_empty_label_size_is_unchanged(self):
        # ApparelSize's validator rewrites an empty labelSize to "-" / "CUSTOM";
        # get_size returned "-" before and must keep doing so.
        part = gen_sized_part("P1", "", None)
        assert part.ApparelSize.labelSize == "-"
        assert part.ApparelSize.customSize == "CUSTOM"
        assert part.get_size() == "-"


class TestProductPartGetSizeOffSpecPath:
    """labelSize is a normal token AND customSize is filled: honor customSize only
    when it is a standard size DIFFERENT from the label, as the spec token."""

    # --- customSize names a different size: it wins, as the spec token ---

    def test_a4_xxs_under_xs_label(self):
        # A4 / Boxercraft / Wholesale Printables: labelSize "XS" + customSize "XXS".
        assert gen_sized_part("NB5294 SCR XXS", "XS", "XXS").get_size() == "2XS"

    def test_custom_size_case_is_ignored(self):
        assert gen_sized_part("P1", "XS", "xxs").get_size() == "2XS"

    def test_label_case_is_ignored_in_the_comparison(self):
        assert gen_sized_part("P1", "xs", "XXS").get_size() == "2XS"

    def test_custom_size_already_a_spec_token(self):
        assert gen_sized_part("P1", "XS", "2XS").get_size() == "2XS"

    def test_other_neighbouring_sizes(self):
        assert gen_sized_part("P1", "S", "XS").get_size() == "XS"
        assert gen_sized_part("P2", "M", "LARGE").get_size() == "L"

    # --- customSize is the same size spelled differently: label wins ---

    def test_same_size_spelled_differently_keeps_label(self):
        # Colosseum 2XL + "XXL"/"Xxl", Royal Apparel 2XL + "2X", Pennant S + "SM",
        # Pearsox M + "MEDIUM", Champro L + "Large" / M + "Medium".
        assert gen_sized_part("P1", "2XL", "XXL").get_size() == "2XL"
        assert gen_sized_part("P2", "2XL", "Xxl").get_size() == "2XL"
        assert gen_sized_part("P3", "2XL", "2X").get_size() == "2XL"
        assert gen_sized_part("P4", "S", "SM").get_size() == "S"
        assert gen_sized_part("P5", "M", "MEDIUM").get_size() == "M"
        assert gen_sized_part("P6", "L", "Large").get_size() == "L"
        assert gen_sized_part("P7", "M", "Medium").get_size() == "M"
        assert gen_sized_part("P8", "OSFA", "ONE SIZE").get_size() == "OSFA"

    def test_identical_values_keep_label(self):
        assert gen_sized_part("P1", "XS", "XS").get_size() == "XS"
        assert gen_sized_part("P2", "2XL", "2xl").get_size() == "2XL"

    @pytest.mark.parametrize("alias, token", sorted(SIZE_ALIASES.items()))
    def test_an_alias_never_overrides_its_own_target(self, alias, token):
        assert gen_sized_part("P1", token, alias).get_size() == token

    # --- customSize is not a standard size: label wins ---

    def test_champro_combo_sizes_keep_label(self):
        # Champro HC7 ladder: XS/S, S/M, L/XL under XS/S/L; CUSTOM + "2XL" on top.
        assert gen_sized_part("HC7B1XSS", "XS", "XS/S").get_size() == "XS"
        assert gen_sized_part("HC7B1SM", "S", "S/M").get_size() == "S"
        assert gen_sized_part("HC7B1LXL", "L", "L/XL").get_size() == "L"
        assert gen_sized_part("HC7B1XXL", "CUSTOM", "2XL").get_size() == "2XL"
        assert gen_sized_part("P5", "M", "M/L").get_size() == "M"
        assert gen_sized_part("P6", "XS", "XXS/XS").get_size() == "XS"

    def test_filler_and_numeric_keep_label(self):
        assert gen_sized_part("P1", "S", "NA").get_size() == "S"   # SanMar Canada
        assert gen_sized_part("P2", "S", "32").get_size() == "S"

    @pytest.mark.parametrize("value", FREE_TEXT_SIZES)
    def test_any_free_text_keeps_label(self, value):
        assert gen_sized_part("P1", "M", value).get_size() == "M"

    # --- the label itself is off-spec: keep it, it carries more information ---

    def test_off_spec_label_beats_a_standard_custom_size(self):
        assert gen_sized_part("P1", "L/XL", "XL").get_size() == "L/XL"
        assert gen_sized_part("P2", "L/XL", "NA").get_size() == "L/XL"

    # --- invariants ---

    @pytest.mark.parametrize("label", [None, "", "  ", "CUSTOM", "custom", "XS", "xs",
                                       "2XL", "XXL", "L/XL", "-"])
    @pytest.mark.parametrize("custom", [None, "", "  ", "CUSTOM", "XS", "XXS", "2XS",
                                        "XXL", "S/M", "42R", "NA"])
    def test_get_size_never_returns_none(self, label, custom):
        result = gen_sized_part("P1", label, custom).get_size()
        assert isinstance(result, str)


class TestGetSizeIntegration:
    """The token integrates with the rest of psdomain: counting and sorting."""

    def test_a4_xxs_and_xs_parts_of_same_color_are_distinct(self):
        # Regression for the HIT a Double duplicate: both parts read as "XS" before,
        # so the importer dropped one and Add New Variants re-created it later.
        xxs = gen_sized_part("NB5294 SCR XXS", "XS", "XXS")
        xs = gen_sized_part("NB5294 SCR XS", "XS", None)
        assert xxs.get_primary_color() == xs.get_primary_color()
        assert {xxs.get_size(), xs.get_size()} == {"2XS", "XS"}

    def test_get_number_of_sizes_counts_the_a4_pair_as_two(self):
        arr = ProductPartArray(ProductPart=[
            gen_sized_part("NB5294 SCR XXS", "XS", "XXS"),
            gen_sized_part("NB5294 SCR XS", "XS", None),
            gen_sized_part("NB5294 SCR S", "S", None),
        ])
        assert arr.get_number_of_sizes() == 3

    def test_sort_sizes_places_2xs_before_xs(self):
        # Returning the spec token (not "XXS") is what lets the A4 part sort.
        parts = [
            gen_sized_part("NB5294 SCR S", "S", None),
            gen_sized_part("NB5294 SCR XS", "XS", None),
            gen_sized_part("NB5294 SCR XXS", "XS", "XXS"),
        ]
        assert [p.get_size() for p in sort_sizes(parts)] == ["2XS", "XS", "S"]

    def test_champro_hc7_ladder_unchanged(self):
        parts = [
            gen_sized_part("HC7B1XSS", "XS", "XS/S"),
            gen_sized_part("HC7B1SM", "S", "S/M"),
            gen_sized_part("HC7B1LXL", "L", "L/XL"),
            gen_sized_part("HC7B1XXL", "CUSTOM", "2XL"),
        ]
        assert [p.get_size() for p in parts] == ["XS", "S", "L", "2XL"]
        assert [p.get_size() for p in sort_sizes(parts)] == ["XS", "S", "L", "2XL"]
