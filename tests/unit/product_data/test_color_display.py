"""Display colour name and colour grouping for product parts.

Real feed values:
  * SanMar 5000 spells the same colour two ways: "Antqu Chry Red" on S..3XL and
    "AntqChryRd" on 4XL, while standardColorName is "Antique Cherry Red" on both.
    Grouping by colorName showed 107 "colours" for an 80-colour product.
  * A4, Champro and most other suppliers file the generic PromoStandards bucket in
    standardColorName ("CARDINAL" -> "Red", "BLACK/WHITE" -> "Multicolor"), so the
    standard name must never replace a legible colorName.
"""
import pytest

from psdomain.model.product_data.common import (
    ProductPart, Color, ColorArray, PrimaryColor, ProductPartArray, ApparelSize, ApparelStyle,
    is_legible_color_name, get_display_color_name, expand_color_abbreviations,
)

from .test_product_part import default_values


def gen_part(part_id, color_name, standard=None, size=None, hex_val=None, closeout=None):
    values = default_values.copy()
    if size:
        values["ApparelSize"] = ApparelSize(apparelStyle=ApparelStyle.Unisex, labelSize=size, customSize=None)
    values["ColorArray"] = ColorArray(Color=[Color(
        colorName=color_name, hex=hex_val, approximatePms=None, standardColorName=standard)])
    values["isCloseout"] = closeout
    return ProductPart(partId=part_id, description=[color_name], **values)


class TestIsLegibleColorName:
    @pytest.mark.parametrize("name", [
        "Black", "Cardinal Red", "CAROLINA BLUE", "Antique Cherry Red", "Black/White",
        "Heather Grey", "Sky Blue", "Navy", "Athletic Orange 2011", "Dusty Lilac- New!",
        "Royal", "Kelly Green", "Ash", "Coral Silk", "Brown Savana", "UNTUCKit Navy (576)",
    ])
    def test_plain_words_are_legible(self, name):
        assert is_legible_color_name(name) is True

    @pytest.mark.parametrize("name", [
        "AntqChryRd",      # camelCase run of truncations (SanMar 4XL)
        "CardinalRd",      # camelCase boundary
        "CoralSilk",       # camelCase, even though both words are complete
        "DkChoc",          # abbreviations
        "Antqu Chry Red",  # "Chry" has no vowel
        "Antqu Irish Gn",  # "Gn" has no vowel
        "Lt Blue",         # abbreviation table
        "Dk. Green",       # abbreviation with a trailing dot
        "Hthr Grey",       # abbreviation table
        "FanMrnGrn",
        "SOrange",         # upper-upper-lower boundary
    ])
    def test_abbreviated_names_are_not_legible(self, name):
        assert is_legible_color_name(name) is False

    @pytest.mark.parametrize("name", ["", None, "   "])
    def test_empty_is_not_legible(self, name):
        assert is_legible_color_name(name) is False


class TestExpandColorAbbreviations:
    def test_expands_known_tokens(self):
        assert expand_color_abbreviations("Dk Grn") == "Dark Green"
        assert expand_color_abbreviations("Lt. Blue") == "Light Blue"

    def test_splits_camel_case(self):
        assert expand_color_abbreviations("DkChoc") == "Dark Chocolate"
        assert expand_color_abbreviations("ForestGrn") == "Forest Green"

    def test_keeps_unknown_tokens_and_separators(self):
        assert expand_color_abbreviations("Blk/Wht") == "Black/White"
        assert expand_color_abbreviations("Chry Red") == "Chry Red"

    def test_drops_the_word_a_code_prefix_expands_to(self):
        # Midwest Workwear: "NV-Navy", "WH-White".
        assert expand_color_abbreviations("NV-Navy") == "Navy"
        assert expand_color_abbreviations("WH-White") == "White"
        assert expand_color_abbreviations("Navy-White") == "Navy-White"


class TestGetDisplayColorName:
    # --- standard name is an expansion of colorName: it wins, even when legible ---

    @pytest.mark.parametrize("color_name, standard, expected", [
        ("AntqChryRd", "Antique Cherry Red", "Antique Cherry Red"),
        ("Antqu Chry Red", "Antique Cherry Red", "Antique Cherry Red"),
        ("Antqu Jade Dom", "Antique Jade Dome", "Antique Jade Dome"),
        ("AntqJadeDm", "Antique Jade Dome", "Antique Jade Dome"),
        ("Antqu Irish Gn", "Antique Irish Green", "Antique Irish Green"),
        ("CarolinaBl", "Carolina Blue", "Carolina Blue"),
        ("CAROLINA BLUE", "Carolina Blue", "Carolina Blue"),
        ("Cardinal Red", "Cardinal Red", "Cardinal Red"),
        ("CardinalRd", "Cardinal Red", "Cardinal Red"),
        ("Lt Blue", "Light Blue", "Light Blue"),
        ("FanMrnGrn", "Fan Marine Green", "Fan Marine Green"),
        ("DkChoc", "Dark Chocolate", "Dark Chocolate"),
        ("Blu", "Blue", "Blue"),
        ("SOrange", "S. Orange", "S. Orange"),   # SanMar Safety Orange, 4XL
        ("S Orange", "S. Orange", "S. Orange"),
    ])
    def test_standard_name_that_expands_color_name_wins(self, color_name, standard, expected):
        assert get_display_color_name(color_name, standard) == expected

    # --- legible colorName beats a generic bucket ---

    @pytest.mark.parametrize("color_name, standard, expected", [
        ("CARDINAL", "Red", "Cardinal"),
        ("CHARCOAL", "Black", "Charcoal"),
        ("BLACK/WHITE", "Multicolor", "Black/White"),
        ("Fire Red", "Red", "Fire Red"),
        ("Forest", "Green", "Forest"),
        ("Navy", "Blue", "Navy"),
        ("Heather Grey", "Gray", "Heather Grey"),
        ("Athletic Orange 2011", "Orange", "Athletic Orange 2011"),
    ])
    def test_legible_color_name_beats_bucket(self, color_name, standard, expected):
        assert get_display_color_name(color_name, standard) == expected

    def test_legible_color_name_beats_a_descriptive_but_different_standard(self):
        # A richer supplier name is never replaced by a shorter standard one.
        assert get_display_color_name("Dark Heather Navy", "Navy") == "Dark Heather Navy"

    # --- not legible: descriptive standard name, then the abbreviation table ---

    def test_abbreviated_color_name_uses_descriptive_standard(self):
        # SanMar 5000: "ForestGrn" (4XL, 5XL) and "Forest" (S..3XL) share standard "Forest".
        assert get_display_color_name("ForestGrn", "Forest") == "Forest"
        assert get_display_color_name("Forest", "Forest") == "Forest"

    @pytest.mark.parametrize("color_name, standard, expected", [
        ("DkGrn", "Green", "Dark Green"),        # bucket: expand the abbreviation instead
        ("Lt. Pnk", "Pink", "Light Pink"),
        ("Hthr Gry", "Gray", "Heather Gray"),
        ("Blk/Wht", "Multicolor", "Black/White"),
        ("LT BLUE/WHITE", "Multicolor", "Light Blue/White"),   # A4: title-cased before expanding
        ("NV-Navy", "Blue", "Navy"),
        ("DkChoc", None, "Dark Chocolate"),
        ("DkChoc", "", "Dark Chocolate"),
    ])
    def test_abbreviated_color_name_with_bucket_or_no_standard_is_expanded(self, color_name, standard, expected):
        assert get_display_color_name(color_name, standard) == expected

    def test_unknown_abbreviation_is_returned_unchanged(self):
        assert get_display_color_name("Chry Red", "Red") == "Chry Red"

    # --- casing ---

    def test_all_caps_name_is_title_cased(self):
        assert get_display_color_name("CAROLINA BLUE", None) == "Carolina Blue"
        assert get_display_color_name("BLACK", "Black") == "Black"

    def test_mixed_case_name_is_kept_verbatim(self):
        assert get_display_color_name("Dusty Lilac- New!", "Purple") == "Dusty Lilac- New!"
        assert get_display_color_name("Brown Savana", "Brown Savana") == "Brown Savana"

    @pytest.mark.parametrize("color_name, standard", [(None, None), ("", ""), (None, "Red"), ("  ", "Red")])
    def test_missing_color_name_gives_empty(self, color_name, standard):
        assert get_display_color_name(color_name, standard) == ""

    def test_whitespace_is_stripped(self):
        assert get_display_color_name("  Black ", " Black ") == "Black"


class TestProductPartDisplayColor:
    def test_uses_first_color_of_the_array(self):
        part = gen_part("P1", "AntqChryRd", "Antique Cherry Red")
        assert part.get_display_color() == "Antique Cherry Red"
        assert part.get_primary_color() == "AntqChryRd"  # unchanged: exporters rely on it

    def test_falls_back_to_primary_color(self):
        values = default_values.copy()
        values["ColorArray"] = None
        values["primaryColor"] = PrimaryColor(Color=Color(colorName="DkChoc", standardColorName="Brown"))
        part = ProductPart(partId="P1", description=["x"], **values)
        assert part.get_display_color() == "Dark Chocolate"

    def test_no_color_at_all(self):
        values = default_values.copy()
        values["ColorArray"] = None
        part = ProductPart(partId="P1", description=["x"], **values)
        assert part.get_display_color() == ""
        assert part.get_color_key() == ""

    def test_color_key_is_case_insensitive(self):
        assert gen_part("P1", "CAROLINA BLUE", "Carolina Blue").get_color_key() == \
            gen_part("P2", "CarolinaBl", "Carolina Blue").get_color_key()


class TestGroupByColor:
    """SanMar 5000 slice: 3 colours spelled 6 ways across 8 parts."""

    def parts(self):
        return [
            gen_part("2489331", "AntqChryRd", "Antique Cherry Red", "4XL"),
            gen_part("705171", "Antqu Chry Red", "Antique Cherry Red", "2XL", hex_val="7C2529"),
            gen_part("705164", "Antqu Chry Red", "Antique Cherry Red", "L", hex_val="7C2529"),
            gen_part("705162", "Antqu Chry Red", "Antique Cherry Red", "S", hex_val="7C2529", closeout=True),
            gen_part("F4XL", "ForestGrn", "Forest", "4XL"),
            gen_part("FS", "Forest", "Forest", "S"),
            gen_part("CB4XL", "CarolinaBl", "Carolina Blue", "4XL"),
            gen_part("CBS", "CAROLINA BLUE", "Carolina Blue", "S"),
        ]

    def test_groups_the_spellings_together_in_first_seen_order(self):
        groups = ProductPartArray(ProductPart=self.parts()).group_by_color()
        assert [g.name for g in groups] == ["Antique Cherry Red", "Forest", "Carolina Blue"]
        assert [len(g.parts) for g in groups] == [4, 2, 2]

    def test_parts_within_a_group_are_sorted_by_size(self):
        groups = ProductPartArray(ProductPart=self.parts()).group_by_color()
        assert [p.partId for p in groups[0].parts] == ["705162", "705164", "705171", "2489331"]
        assert groups[0].sizes == ["S", "L", "2XL", "4XL"]

    def test_group_hex_is_the_first_available(self):
        groups = ProductPartArray(ProductPart=self.parts()).group_by_color()
        assert groups[0].hex == "7C2529"
        assert groups[1].hex is None

    def test_group_closeout_flags(self):
        groups = ProductPartArray(ProductPart=self.parts()).group_by_color()
        assert groups[0].has_closeout is True
        assert groups[0].all_closeout is False
        assert groups[1].has_closeout is False

    def test_number_of_colors_counts_groups_not_spellings(self):
        arr = ProductPartArray(ProductPart=self.parts())
        assert arr.get_number_of_colors() == 3

    def test_parts_without_color_form_one_unnamed_group(self):
        values = default_values.copy()
        values["ColorArray"] = None
        bare = ProductPart(partId="B1", description=["x"], **values)
        groups = ProductPartArray(ProductPart=[bare, gen_part("P1", "Black")]).group_by_color()
        assert [g.name for g in groups] == ["", "Black"]

    def test_empty_array(self):
        assert ProductPartArray(ProductPart=[]).group_by_color() == []
        assert ProductPartArray(ProductPart=[]).get_number_of_colors() == 0
