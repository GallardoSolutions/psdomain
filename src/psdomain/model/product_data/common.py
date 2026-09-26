import re
import typing
from datetime import datetime
from decimal import Decimal

from pydantic import Field, model_validator, field_validator

from .. import base
from ..base import StrEnum


def get_normalized_category(category: str) -> str:
    ret = category.strip().title().replace('&Amp;', '&amp;') if category else ''
    return ret if ret != '-' else ''


# PromoStandards labelSize vocabulary (Product Data 2.0 ApparelSize).
STANDARD_SIZES = frozenset({
    "OSFA", "6XS", "5XS", "4XS", "3XS", "2XS", "XS", "S", "M", "L", "XL",
    "2XL", "3XL", "4XL", "5XL", "6XL",
})

# Spellings suppliers put in customSize NEXT TO a normal labelSize, mapped to the
# spec token. Only spellings seen in real feeds: A4/Boxercraft "XXS", Colosseum
# "XXL", Royal Apparel "2X", Pennant "SM/MD/LG", Pearsox "MEDIUM".
SIZE_ALIASES = {
    "XXS": "2XS", "XXXS": "3XS",
    "XXL": "2XL", "XXXL": "3XL", "XXXXL": "4XL",
    "2X": "2XL", "3X": "3XL", "4X": "4XL", "5X": "5XL",
    "SM": "S", "MD": "M", "LG": "L",
    "SMALL": "S", "MEDIUM": "M", "LARGE": "L",
    "EXTRA SMALL": "XS", "EXTRA LARGE": "XL",
    "ONE SIZE": "OSFA", "OSFM": "OSFA",
}


def canonical_size(value: str | None) -> str | None:
    """The spec token for a size spelling, or None when the value is not a
    recognizable standard size (free text such as "S/M", "42R", "NA")."""
    if not value:
        return None
    token = value.strip().upper().replace("-", "")
    token = SIZE_ALIASES.get(token, token)
    return token if token in STANDARD_SIZES else None


class ProductCategory(base.PSBaseModel):
    category: str | None
    subCategory: str | None

    @property
    def full_category(self):
        category = get_normalized_category(self.category)
        sub_category = get_normalized_category(self.subCategory)
        if category:
            if sub_category:
                return f'{category} > {sub_category}'
            return category
        return sub_category if sub_category else 'Unknown'


class ProductCategoryArray(base.PSBaseModel):
    ProductCategory: list[ProductCategory]


class RelationTye(StrEnum):
    Substitute = 'Substitute'
    CompanionSell = 'Companion Sell'
    CommonGrouping = 'Common Grouping'


class RelatedProduct(base.PSBaseModel):
    relationType: RelationTye
    productId: str
    partId: str | None

    @property
    def is_substitute(self):
        return self.relationType == RelationTye.Substitute

    @property
    def is_companion_sell(self):
        return self.relationType == RelationTye.CompanionSell

    @property
    def is_common_grouping(self):
        return self.relationType == RelationTye.CommonGrouping

    @field_validator('relationType', mode='before')
    @classmethod
    def map_invalid_relation_type(cls, v):
        if isinstance(v, str):
            if v.strip().lower() == "you may also like":
                return RelationTye.Substitute
        return v


class RelatedProductArray(base.PSBaseModel):
    RelatedProduct: list[RelatedProduct]


class ApparelStyle(StrEnum):
    Unisex = 'Unisex'
    Youth = 'Youth'
    Girls = 'Girls'
    Boys = 'Boys'
    Womens = 'Womens'
    WomensTall = 'WomensTall'
    Mens = 'Mens'
    MensTall = 'MensTall'

    @classmethod
    def kids(cls):
        return ApparelStyle.Youth, ApparelStyle.Boys, ApparelStyle.Girls

    @classmethod
    def adults(cls):
        return ApparelStyle.Womens, ApparelStyle.WomensTall, ApparelStyle.Mens, ApparelStyle.MensTall

    @property
    def is_unisex(self):
        return self == ApparelStyle.Unisex

    @property
    def is_male(self):
        return self in (ApparelStyle.Mens, ApparelStyle.MensTall, ApparelStyle.Boys)

    @property
    def is_female(self):
        return self in (ApparelStyle.Womens, ApparelStyle.WomensTall, ApparelStyle.Girls)


class ApparelSize(base.PSBaseModel):
    apparelStyle: ApparelStyle
    labelSize: str
    customSize: str | None

    @model_validator(mode='before')
    @classmethod
    def fill_missing_label_size(cls, data):
        # Showdown Displays is sending empty labelSize
        if isinstance(data, dict):
            label = data.get('labelSize')
            if not label or not label.strip():
                data['labelSize'] = '-'
                data['customSize'] = 'CUSTOM'
        else:
            label = data.labelSize
            if not label or not label.strip():
                data.labelSize = '-'
                data.customSize = 'CUSTOM'
        return data

    @property
    def google_age_group(self) -> str:
        """
        newborn
        infant
        toddler
        kids
        adult
        unisex can be kids or adult however we will use adult by default
        """
        if self.apparelStyle in ApparelStyle.kids():
            return 'kids'
        if self.apparelStyle in ApparelStyle.adults():
            return 'adult'
        return 'adult'

    @property
    def google_gender(self) -> str:
        """
        Male [male]
        Female [female]
        Unisex [unisex]
        :return:
        """
        if self.apparelStyle.is_female:
            return 'female'
        if self.apparelStyle.is_male:
            return 'male'
        if self.apparelStyle.is_unisex:
            return 'unisex'
        return 'unisex'  # default to unisex


class Dimension(base.PSBaseModel):
    dimensionUom: base.DimensionUoM | None
    depth: Decimal | None
    height: Decimal | None
    width: Decimal | None
    weightUom: base.WeightUoM | None
    weight: Decimal | None


class ProductPackage(base.PSBaseModel):
    default: bool
    packageType: str | None  # Ariel has at least 1 product with None(DTM-MB24)
    description: str | None
    quantity: Decimal
    dimensionUom: base.DimensionUoM
    depth: Decimal | None
    height: Decimal | None
    width: Decimal | None
    weightUom: base.WeightUoM
    weight: Decimal | None


class ProductPackagingArray(base.PSBaseModel):
    ProductPackage: list[ProductPackage]


class ShippingPackage(base.PSBaseModel):
    packageType: str | None  # required by the spec, but Aakron sends null for every part (2026-09-12)
    description: str | None
    quantity: Decimal
    dimensionUom: base.DimensionUoM
    depth: Decimal | None
    height: Decimal | None
    width: Decimal | None
    weightUom: base.WeightUoM
    weight: Decimal | None


class ShippingPackageArray(base.PSBaseModel):
    ShippingPackage: list[ShippingPackage]


class Color(base.PSBaseModel):
    colorName: str | None  # The color name is not required in the WSDL and SNUGZ have some products with None
    hex: str | None = None
    approximatePms: str | None = None
    standardColorName: str | None = None


class PrimaryColor(base.PSBaseModel):
    Color: Color


class ColorArray(base.PSBaseModel):
    Color: list[Color]

    @field_validator('Color', mode='before')
    def drop_null_entries(cls, value):
        # EVANS answers "Color": [null] on some parts (product 1974, 2026-09-12); a null entry
        # is no colour at all, not a reason to reject the whole product.
        if isinstance(value, list):
            return [item for item in value if item is not None]
        return value


# Generic buckets suppliers file in standardColorName (the PromoStandards standard colour list
# plus the spellings seen in real feeds). A bucket says what family a colour belongs to; it is
# never a better display name than the supplier's own colorName.
STANDARD_COLOR_BUCKETS = frozenset({
    'assorted', 'beige', 'black', 'blue', 'brown', 'camouflage', 'camo', 'clear', 'custom', 'gold', 'gray',
    'grey', 'green', 'heather', 'metallic', 'multi', 'multicolor', 'multi-color', 'multi color', 'multicolour',
    'natural', 'orange', 'other', 'peach', 'pink', 'purple', 'rainbow', 'red', 'silver', 'tan', 'white',
    'yellow', 'sample', 'design for sample', 'no match',
})

# S&S files unmatched colours as "ZZZ - Multi Color" / "ZZZ - No Match".
_PLACEHOLDER_STANDARD_PREFIX = 'zzz'

# Abbreviations suppliers use inside colorName tokens (Champro, A4, SanMar 4XL+ SKUs). "Gr" is
# deliberately absent: SanMar uses it for Green ("Kelly Gr") and Graphite as often as for Grey.
COLOR_ABBREVIATIONS = {
    'lt': 'Light', 'dk': 'Dark', 'md': 'Medium', 'med': 'Medium', 'hthr': 'Heather', 'hth': 'Heather', 'htr': 'Heather',
    'choc': 'Chocolate', 'ylw': 'Yellow', 'grn': 'Green', 'brn': 'Brown', 'org': 'Orange', 'fl': 'Fluorescent',
    'wht': 'White', 'blk': 'Black', 'blck': 'Black', 'rd': 'Red', 'nv': 'Navy', 'nvy': 'Navy', 'prpl': 'Purple',
    'pnk': 'Pink', 'slvr': 'Silver', 'gld': 'Gold', 'mrn': 'Maroon', 'ntrl': 'Natural', 'gry': 'Gray',
    'roy': 'Royal', 'ryl': 'Royal', 'chr': 'Charcoal', 'char': 'Charcoal', 'antq': 'Antique',
    'antqu': 'Antique', 'bl': 'Blue', 'blu': 'Blue', 'wh': 'White',
}

# Supplier colour codes glued in front of the name: S&S "GY-Grey", "KB-Khaki/ Black Microcheck",
# Midwest Workwear "NV-Navy", OTTO "025 - Char. Gray", Champro "LB7 - LT BLUE, WHITE".
# "T-Shirt", "3-Month", "12-Sheet" are not codes: one character never is, and digits only are when
# spaced ("003 - Black").
_HYPHEN_CODE_PREFIX = re.compile(r'^(?P<code>[A-Z0-9]{2,4})(?P<sep>\s*-\s*)(?=[A-Za-z])')
# A leading code or brand tag before a space is kept but ignored when judging legibility:
# S&S "CS Grey Light Heather/ White", HIT "FSC BLACK", SanMar "TNF Black" (The North Face).
_SPACE_CODE_PREFIX = re.compile(r'^(?P<code>[A-Z]{2,3})\s+(?=[A-Za-z])')

# Short real words with no a/e/i/o/u that must not read as abbreviations.
_VOWELLESS_COLOR_WORDS = frozenset({'sky', 'gym', 'lynx', 'ivy'})

# "CardinalRd" and "SOrange" (SanMar's Safety Orange) are both camelCase runs; a single leading
# capital counts, a longer run does not ("UNTUCKit" is a brand, not an abbreviation).
_CAMEL_BOUNDARY = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<![A-Za-z][A-Z])(?<=[A-Z])(?=[A-Z][a-z])')
_COLOR_TOKEN_SPLIT = re.compile(r'([\s/,&+\-]+)')


def _color_tokens(name: str) -> list[str]:
    """Word tokens of a colour name, with camelCase runs split ("AntqChryRd" -> Antq, Chry, Rd)."""
    tokens = []
    for chunk in _COLOR_TOKEN_SPLIT.split(name):
        if not chunk or _COLOR_TOKEN_SPLIT.fullmatch(chunk):
            continue
        tokens.extend(t for t in _CAMEL_BOUNDARY.split(chunk) if t)
    return tokens


def _is_abbreviation(token: str) -> bool:
    word = token.rstrip('.!').lower()
    if not word.isalpha():
        return False  # "2011", "#1" and the like say nothing about legibility
    if word in COLOR_ABBREVIATIONS:
        return True
    if word in _VOWELLESS_COLOR_WORDS:
        return False
    return len(word) >= 2 and not any(ch in 'aeiou' for ch in word)


def is_legible_color_name(name: str | None) -> bool:
    """True when a colour name reads as plain words: no camelCase runs ("CardinalRd"), no
    vowel-less truncations ("Chry", "Gn") and no known abbreviations ("Lt", "Dk", "Hthr")."""
    if not name or not name.strip():
        return False
    name = name.strip()
    if _CAMEL_BOUNDARY.search(name):
        return False
    m = _SPACE_CODE_PREFIX.match(name)
    if m and _is_code(m.group('code')):
        name = name[m.end():]  # "TNF Black", "FSC BLACK": judge the name after the tag
    return not any(_is_abbreviation(t) for t in _color_tokens(name))


def expand_color_abbreviations(name: str) -> str:
    """"DkGrn" -> "Dark Green", "Blk/Wht" -> "Black/White". Unknown tokens are kept, and so are
    repeated panels ("Blk/Blk/Wht" is a three-panel cap, not a typo)."""
    out = []
    for chunk in _COLOR_TOKEN_SPLIT.split(name.strip()):
        if not chunk:
            continue
        if _COLOR_TOKEN_SPLIT.fullmatch(chunk):
            out.append(chunk)
            continue
        words = [COLOR_ABBREVIATIONS.get(t.rstrip('.').lower(), t) for t in _CAMEL_BOUNDARY.split(chunk) if t]
        out.append(' '.join(words))
    return ''.join(out)


def _is_code(token: str) -> bool:
    """A supplier code, not a word: has a digit ("LB7", "025") or no vowel ("GY", "FSC") and is
    not an abbreviation we would rather expand ("Dk", "Wh")."""
    word = token.lower()
    if word in COLOR_ABBREVIATIONS or word in _VOWELLESS_COLOR_WORDS:
        return False  # "Dk" should be expanded, "Sky" is a word
    return any(ch.isdigit() for ch in word) or not any(ch in 'aeiou' for ch in word)


def strip_color_code_prefix(name: str) -> str:
    """Drop a supplier colour code glued to the name with a hyphen: "GY-Grey" -> "Grey",
    "025 - Char. Gray" -> "Char. Gray", "NV-Navy" -> "Navy". "RED-WHITE" is left alone (a word),
    and so is "TNF Black": before a space the tag may be a brand, so it stays."""
    name = name.strip()
    m = _HYPHEN_CODE_PREFIX.match(name)
    if m and not (m.group('code').isdigit() and m.group('sep') == '-'):
        code, rest = m.group('code'), name[m.end():]
        expansion = COLOR_ABBREVIATIONS.get(code.lower())
        if expansion is None and _is_code(code):
            return rest
        if expansion is not None and rest.lower().startswith(expansion.lower()):
            return rest  # "NV-Navy", "WH-White": the code is also an abbreviation of the name
    return name


def _is_bucket(standard: str) -> bool:
    """True when standardColorName is a generic family or a placeholder rather than a name."""
    lowered = standard.strip().lower()
    return lowered in STANDARD_COLOR_BUCKETS or lowered.startswith(_PLACEHOLDER_STANDARD_PREFIX)


def _is_subsequence(short: str, long: str) -> bool:
    it = iter(long)
    return all(ch in it for ch in short)


def _expands(color_name: str, standard: str) -> bool:
    """True when `standard` spells out `color_name` token by token: "Antqu Chry Red" and
    "AntqChryRd" are both expanded by "Antique Cherry Red"; "CARDINAL" is not expanded by "Red"."""
    short = [t.lower() for t in _color_tokens(color_name)]
    long = [t.lower() for t in _color_tokens(standard)]
    if not short or len(short) != len(long):
        return False
    return all(a and b and a[0] == b[0] and _is_subsequence(a, b) for a, b in zip(short, long))


def _title_if_shouting(name: str) -> str:
    if not name.isupper():
        return name
    return ' '.join(w if any(ch.isdigit() for ch in w) else w.title() for w in name.split(' '))


def get_display_color_name(color_name: str | None, standard_color_name: str | None) -> str:
    """The most readable name for a part colour, choosing between the supplier's colorName and
    its standardColorName:

    1. standardColorName spells out colorName ("AntqChryRd" / "Antique Cherry Red"): the standard name.
    2. colorName is legible: colorName. A generic bucket ("Red") never replaces "Cardinal".
    3. colorName is abbreviated and standardColorName is descriptive (not a bucket or a
       placeholder such as "ZZZ - Multi Color"): the standard name, which is what stays constant
       across sizes ("ForestGrn" / "Forest").
    4. Otherwise colorName with its abbreviations expanded ("DkGrn" -> "Dark Green").

    A hyphenated supplier code in front of the name is dropped first ("GY-Grey" becomes "Grey");
    a tag before a space is kept but does not make the name abbreviated ("TNF Black").
    All-caps names are title-cased. Empty colorName gives ''.
    """
    color_name = strip_color_code_prefix(color_name or '')
    standard = (standard_color_name or '').strip()
    if not color_name:
        return ''
    if standard and _expands(color_name, standard):
        return _title_if_shouting(standard)
    if is_legible_color_name(color_name):
        return _title_if_shouting(color_name)
    if standard and not _is_bucket(standard):
        return _title_if_shouting(standard)
    return expand_color_abbreviations(_title_if_shouting(color_name))


class SpecificationType(StrEnum):
    Length = 'Length'
    Thickness = 'Thickness'
    Radius = 'Radius'
    Volume = 'Volume'
    Capacity = 'Capacity'
    Memory = 'Memory'
    DataPorts = 'Data Ports'
    Capacitance = 'Capacitance'
    Voltage = 'Voltage'
    PointSize = 'Point Size'
    SheetSize = 'Sheet Size'
    SheetCount = 'Sheet Count'
    Pockets = 'Pockets'
    Inseam = 'Inseam'
    Bust = 'Bust'
    Chest = 'Chest'
    Waist = 'Waist'
    Hips = 'Hips'
    Cup = 'Cup'
    Rise = 'Rise'
    Neck = 'Neck'
    Thigh = 'Thigh'
    Shoulders = 'Shoulders'
    Sleeve = 'Sleeve'
    DeviceSize = 'Device Size'


class Specification(base.PSBaseModel):
    specificationType: SpecificationType
    SpecificationUom: str | None  # The doc & wsdl says it is required but Sun Joy is returning None for some products
    measurementValue: str | None


class SpecificationArray(base.PSBaseModel):
    Specification: list[Specification]


class ProductPart(base.PSBaseModel):
    websiteUrl: str | None = Field(default=None, description='The URL of the product part in the supplier website')
    partId: str
    description: list[str]
    countryOfOrigin: str | None
    primaryMaterial: str | None
    SpecificationArray: SpecificationArray | None
    shape: str | None
    ApparelSize: ApparelSize | None
    Dimension: Dimension | None
    leadTime: int | None
    unspsc: str | None
    gtin: str | None
    isRushService: bool | None
    endDate: datetime | None
    effectiveDate: datetime | None
    isCloseout: bool | None
    isCaution: bool | None
    cautionComment: str | None
    nmfcCode: Decimal | None
    nmfcDescription: str | None
    nmfcNumber: str | None
    isOnDemand: bool | None
    isHazmat: bool | None
    primaryColor: PrimaryColor | None = None  # in V1 is not required
    ColorArray: ColorArray | None
    ProductPackagingArray: ProductPackagingArray | None
    ShippingPackageArray: ShippingPackageArray | None
    map: Decimal | None = Field(default=None, description='Minimum Advertised Price for the product part(Extra API)')

    def _get_colors(self) -> list[Color]:
        return self.ColorArray.Color if self.ColorArray else []

    def _set_colors(self, colors: list[Color]):
        self.ColorArray = ColorArray(Color=colors)

    Color = property(_get_colors, _set_colors)

    def get_size(self) -> str:
        apparel_size = self.ApparelSize
        if not apparel_size:
            return ''
        label_size = (apparel_size.labelSize or '').strip()
        custom_size = (apparel_size.customSize or '').strip()

        # Spec path: customSize carries the size when the label is CUSTOM.
        if label_size.upper() == 'CUSTOM':
            return custom_size

        # Off-spec path. Some suppliers file a size the vocabulary already has
        # under a neighbouring label and keep the real size in customSize (A4
        # and Boxercraft: labelSize "XS" + customSize "XXS"), which makes two
        # distinct parts read as the same Color/Size. Honor customSize only when
        # it is a standard size DIFFERENT from the label, and return the spec
        # token so it sorts and builds SKUs like every other size.
        # Both sides must be standard sizes: an off-spec label (SanMar Canada's
        # "L/XL") already carries more information than any token and is kept.
        #   XS   + "XXS"  -> "2XS"   (different size: use it)
        #   2XL  + "XXL"  -> "2XL"   (same size spelled differently: keep label)
        #   S    + "S/M"  -> "S"     (not a standard size: keep label)
        #   S    + "NA"   -> "S"     (junk: keep label)
        #   L/XL + "XL"   -> "L/XL"  (off-spec label: keep label)
        custom_token = canonical_size(custom_size)
        label_token = canonical_size(label_size)
        if custom_token and label_token and custom_token != label_token:
            return custom_token
        return label_size

    def get_apparel_style(self) -> str:
        apparel_size = self.ApparelSize
        if apparel_size:
            return apparel_size.apparelStyle
        return ''

    def _primary_color(self) -> 'Color | None':
        arr = self.ColorArray
        if arr and arr.Color:
            return arr.Color[0]
        return self.primaryColor.Color if self.primaryColor else None

    def get_primary_color(self, color_field: str = 'colorName') -> str:
        """
        Returns the primary color of the product part.
        :param color_field: colorName or standardColorName
        :return:
        """
        primary_color = self._primary_color()
        return getattr(primary_color, color_field) if primary_color else ''

    def get_display_color(self) -> str:
        """The most readable name for the part's primary colour (see get_display_color_name).
        Display only: SKU and option mapping keep using get_primary_color."""
        color = self._primary_color()
        return get_display_color_name(color.colorName, color.standardColorName) if color else ''

    def get_color_key(self) -> str:
        """Case-insensitive key that puts every spelling of one colour in the same group."""
        return self.get_display_color().casefold()


class ColorGroup(typing.NamedTuple):
    """The parts of one colour, in size order."""
    key: str
    name: str
    hex: str | None
    parts: list['ProductPart']

    @property
    def sizes(self) -> list[str]:
        return [p.get_size() for p in self.parts if p.get_size()]

    @property
    def has_closeout(self) -> bool:
        return any(p.isCloseout for p in self.parts)

    @property
    def all_closeout(self) -> bool:
        return bool(self.parts) and all(p.isCloseout for p in self.parts)


class ProductPartArray(base.PSBaseModel):
    ProductPart: list[ProductPart]

    def get_number_of_colors(self) -> int:
        """
        Returns the number of colors available for the product parts.
        :return: int
        """
        return len(self.group_by_color())

    def group_by_color(self) -> list[ColorGroup]:
        """Parts grouped by colour in first-seen order, each group sorted by size. Every spelling
        of a colour lands in one group ("Forest" and "ForestGrn"); parts with no colour share
        the unnamed group."""
        groups: dict[str, list[ProductPart]] = {}
        for part in self.ProductPart or []:
            groups.setdefault(part.get_color_key(), []).append(part)
        return [ColorGroup(key=key, name=parts[0].get_display_color(), hex=self._first_hex(parts),
                           parts=sort_sizes(parts)) for key, parts in groups.items()]

    @staticmethod
    def _first_hex(parts: list[ProductPart]) -> str | None:
        for part in parts:
            color = part._primary_color()
            if color and color.hex:
                return color.hex
        return None

    def get_number_of_sizes(self) -> int:
        """
        Returns the number of sizes available for the product parts.
        :return: int
        """
        if not self.ProductPart:
            return 0
        sizes = {part.get_size() for part in self.ProductPart if part.get_size()}
        return len(sizes)


class ProductPrice(base.PSBaseModel):
    quantityMax: int | None
    quantityMin: int
    price: Decimal
    discountCode: str | None


class ProductPriceArray(base.PSBaseModel):
    ProductPrice: list[ProductPrice]


class ProductPriceGroup(base.PSBaseModel):
    groupName: str | None = None  # minOccurs=0 in the SOAP definition; Goldstar sends null
    currency: str
    description: str | None
    ProductPriceArray: typing.Annotated[typing.Optional[ProductPriceArray], Field(None)]

    @property
    def prices(self):
        return self.ProductPriceArray.ProductPrice if self.ProductPriceArray else []


class ProductPriceGroupArray(base.PSBaseModel):
    ProductPriceGroup: list[ProductPriceGroup]


class ProductKeyword(base.PSBaseModel):
    keyword: str


class ProductKeywordArray(base.PSBaseModel):
    ProductKeyword: list[ProductKeyword]


class LocationDecoration(base.PSBaseModel):
    locationName: str | None = Field(default=None)
    maxImprintColors: int | None = Field(default=None)
    decorationName: str | None = Field(default=None)
    locationDecorationComboDefault: bool = Field(default=False)
    priceIncludes: bool = Field(default=False)

    @model_validator(mode='before')
    def before(cls, values):
        fields = ('priceIncludes', 'locationDecorationComboDefault')
        if isinstance(values, dict):
            for f in fields:
                if values.get(f) is None:
                    values[f] = False
        else:
            for f in fields:
                if getattr(values, f) is None:
                    setattr(values, f, False)
        return values


class LocationDecorationArray(base.PSBaseModel):
    LocationDecoration: list[LocationDecoration]


class FobPoint(base.PSBaseModel):
    fobId: str
    fobPostalCode: str
    fobCity: str | None  # SNUGZ is returning None for products from China
    fobState: str
    fobCountry: str


class FobPointArray(base.PSBaseModel):
    FobPoint: list[FobPoint]


class ProductMarketingPoint(base.PSBaseModel):
    pointType: str | None  # because in the WSDL is not required
    pointCopy: str | None  # because in the WSDL is not required


class ProductMarketingPointArray(base.PSBaseModel):
    ProductMarketingPoint: list[ProductMarketingPoint]


class Product(base.PSBaseModel):
    websiteUrl: str | None = Field(default=None, description='The URL of the product in the supplier website')
    productId: str
    productName: str
    description: list[str] | None = None
    priceExpiresDate: datetime | None = None
    productBrand: str | None = None
    export: bool | None = None
    lastChangeDate: datetime | None = None  # St Regis
    creationDate: datetime | None = None  # St Regis
    endDate: datetime | None = None
    effectiveDate: datetime | None = None
    isCaution: bool | None = None
    cautionComment: str | None = None
    isCloseout: bool | None = None
    lineName: str | None = None
    primaryImageURL: str | None = None
    complianceInfoAvailable: bool | None = None
    unspscCommodityCode: int | None = None
    imprintSize: str | None = None
    defaultSetUpCharge: str | None = None
    defaultRunCharge: str | None = None
    ProductCategoryArray: ProductCategoryArray | None
    RelatedProductArray: RelatedProductArray | None
    ProductPartArray: ProductPartArray
    ProductKeywordArray: ProductKeywordArray | None
    LocationDecorationArray: typing.Optional[LocationDecorationArray] = None  # in V1 is not required
    ProductPriceGroupArray: typing.Optional[ProductPriceGroupArray] = None  # in V1 is not required
    FobPointArray: typing.Optional[FobPointArray] = None  # in V1 is not required
    ProductMarketingPointArray: typing.Optional[ProductMarketingPointArray] | None

    @property
    def pk(self):
        return self.productId  # primary key

    @property
    def available_colors(self) -> list[Color]:
        colors_list = []

        for part in self.parts or []:
            if part.ColorArray and part.ColorArray.Color:
                colors = part.ColorArray.Color
                for color in colors:
                    color_name = color.colorName
                    if color_name not in colors_list:
                        colors_list.append(color)
        return colors_list

    @property
    def variants_per_color(self):
        # useful for detecting variants per color in S&S Activewear and SanMar because they don't send part ids
        ret = {}
        for part in self.parts:
            color = part.get_primary_color()
            if color not in ret:
                ret[color] = []
            ret[color].append(part.partId)
        return ret

    @property
    def sizes(self) -> list[str]:
        sizes_list = []

        for part in self.parts:
            if part.ApparelSize:
                size_name = part.ApparelSize.labelSize
                if size_name not in sizes_list:
                    sizes_list.append(size_name)

        return sizes_list

    @property
    def name(self):
        return self.productName

    @property
    def brand(self):
        return self.productBrand

    @property
    def is_caution(self):
        return self.isCaution or any(pp.isCaution for pp in self.parts if pp.isCaution)

    @property
    def is_closeout(self):
        """Whether the whole product is on closeout.

        True when the supplier's product-level ``isCloseout`` flag is set, or when
        *every* part is on closeout. A product with only *some* closeout parts
        (e.g. a couple of discontinued sizes/colors) is still active overall;
        use :pyattr:`has_closeout` to detect that case.
        """
        if self.isCloseout:
            return True
        parts = self.parts
        return bool(parts) and all(pp.isCloseout for pp in parts)

    @property
    def has_closeout(self):
        """Whether the product or any of its parts is on closeout.

        This is the inclusive check (product-level flag OR any closeout part).
        Useful for surfacing that a still-active product has some closeout
        variants. For the "the whole product is closeout" decision, use
        :pyattr:`is_closeout`.
        """
        return bool(self.isCloseout) or any(pp.isCloseout for pp in self.parts)

    @property
    def line_name(self):
        return self.lineName

    @property
    def primary_image_url(self):
        return self.primaryImageURL

    @property
    def country_of_origin(self):
        fp = self.first_part
        return fp.countryOfOrigin if fp else None

    @property
    def primary_material(self):
        fp = self.first_part
        return fp.primaryMaterial if fp else None

    @property
    def lead_time(self):
        lead_times = [pp.leadTime for pp in self.parts if pp.leadTime is not None]
        if lead_times:
            return min(lead_times)
        return None

    @property
    def is_rush_service(self):
        fp = self.first_part
        return fp.isRushService if fp else None

    @property
    def is_on_demand(self):
        fp = self.first_part
        return fp.isOnDemand if fp else None

    def get_description(self):
        return '/n'.join([desc for desc in self.description])

    def get_html_description(self):
        return '<br>'.join([desc for desc in self.description])

    @property
    def first_part(self):
        parts = self.parts
        return parts[0] if parts else None

    @property
    def parts(self):
        return self.ProductPartArray.ProductPart or []

    def get_variant(self, part_id):
        for variant in self.get_variants():
            if variant.partId == part_id:
                return variant
        return None

    def get_variants(self):
        variants = getattr(self, '_variants', None)
        if variants is None:
            variants = self.parts
            if self.has_sizes():
                variants = sort_sizes(variants)
            setattr(self, '_variants', variants)
        return variants

    def has_sizes(self):
        return any(part.ApparelSize for part in self.parts)

    @property
    def categories(self):
        # todo: check if this is what you want
        cat_set = set()
        for c in self.product_category_list:
            if c.category:
                cat_set.add(c.category)
            if c.subCategory:
                cat_set.add(c.subCategory)
        return '|'.join(list(cat_set)) if cat_set else ''

    @property
    def product_category_list(self):
        return self.ProductCategoryArray.ProductCategory if self.ProductCategoryArray else []

    @property
    def main_category(self):
        ret = 'Unknown'
        lst = self.product_category_list
        if lst:
            return lst[0].full_category
        # use keywords for these cases
        return ret

    @property
    def substitutes(self):
        return [rp for rp in self.related_products if rp.is_substitute]

    @property
    def companions(self):
        return [rp for rp in self.related_products if rp.is_companion_sell]

    @property
    def common_groupings(self):
        return [rp for rp in self.related_products if rp.is_common_grouping]

    @property
    def related_products(self):
        return self.RelatedProductArray.RelatedProduct if self.RelatedProductArray else []

    def get_price_and_cost(self, currency='USD', configuration_type='Decorated',
                           variant: dict | None = None):
        """
        "ProductPriceGroupArray": {
            "ProductPriceGroup": [
                {
                    "groupName": "USD-List-Blank_1",
                    "currency": "USD",
                    "description": "USD-List-Blank_1081-41BK,1081-41BL",
                    "ProductPriceArray": {
                        "ProductPrice": [
                            {
                                "quantityMax": null,
                                "quantityMin": 1,
                                "price": "30.980000000",
                                "discountCode": "C"
                            },
                        ]
                    }
                }
            ]
        }
        variant will be used for PPC, we can get the correct price for variants like Sanmar t-shirts
        """
        product_price_array = self.get_product_price_array(currency, configuration_type)
        price = product_price_array[0].price if product_price_array else None
        cost = get_cost(price, product_price_array[0].discountCode) if price else None
        return price, cost

    def get_list_price(self, currency='USD', configuration_type='Decorated'):
        return self.get_price_and_cost(currency, configuration_type)[0]

    @property
    def price_groups(self):
        return self.ProductPriceGroupArray.ProductPriceGroup if self.ProductPriceGroupArray else []

    def get_product_price_array(self, currency, configuration_type):
        conf_type = configuration_type.lower()
        price_groups = self.price_groups
        filtered_by_currency = [pg for pg in price_groups if pg.currency == currency]
        for price_group in filtered_by_currency:
            if price_group.description and conf_type in price_group.description.lower():
                return price_group.prices
        #
        if filtered_by_currency:
            price_group = filtered_by_currency[0]
        elif price_groups:
            price_group = price_groups[0]
        else:
            return []
        return price_group.prices


class Location(base.PSBaseModel):
    locationId: int
    locationName: str | None


class ProductSellable(base.PSBaseModel):
    productId: str
    partId: str | None
    culturePoint: str | None = None


class ProductSellableArray(base.PSBaseModel):
    ProductSellable: list[ProductSellable]


class ProductDateModified(base.PSBaseModel):
    productId: str
    partId: str | None


class ProductDateModifiedArray(base.PSBaseModel):
    ProductDateModified: list[ProductDateModified]


class ProductCloseOut(base.PSBaseModel):
    productId: str
    partId: str | None


class ProductCloseOutArray(base.PSBaseModel):
    ProductCloseOut: list[ProductCloseOut]


SIZES = ["OSFA", "6XS", "5XS", "4XS", "3XS", "2XS", "XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL",
         "CUSTOM"]

SIZES_INDEX = {size: i for i, size in enumerate(SIZES)} | {'': 1000}


def sort_sizes(variants: list[ProductPart]) -> list[ProductPart]:
    try:
        return sorted(variants, key=lambda v: SIZES_INDEX.get(v.get_size(), v.get_primary_color()))
    except TypeError:  # noqa
        return variants


def get_cost(price, discount_code: str = 'C'):
    if isinstance(price, str):
        price = Decimal(price)
    discount_code = discount_code.upper() if discount_code else 'C'
    # https://cdn.asicentral.com/MKTGemails/401-12988/Codes.pdf
    factors = {
        'A': 50,
        'B': 45,
        'C': 40,
        'D': 35,
        'E': 30,
        'F': 25,
        'G': 20,
        'H': 15,
        'I': 10,
        'J': 5,
        # 'X': 0,  ABC system
        'L': 70,  # PQR system
        'M': 65,
        'N': 60,
        'O': 55,
        'P': 50,
        'Q': 45,
        'R': 40,
        'S': 35,
        'T': 30,
        'U': 25,
        'V': 20,
        'W': 15,
        'X': 10,
        'Y': 5,
        'Z': 0,
    }
    discount = factors.get(discount_code, 40)  # default to 'C' if not found
    ret = price * Decimal(1 - discount / 100)
    return ret.quantize(Decimal('.01'))
