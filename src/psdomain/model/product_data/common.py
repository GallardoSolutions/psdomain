import typing
from datetime import datetime
from decimal import Decimal

from pydantic import Field, model_validator, field_validator

from .. import base
from ..base import StrEnum


def get_normalized_category(category: str) -> str:
    ret = category.strip().title().replace('&Amp;', '&amp;') if category else ''
    return ret if ret != '-' else ''


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
        return self in (ApparelStyle.Mens, ApparelStyle.MensTall)

    @property
    def is_female(self):
        return self in (ApparelStyle.Womens, ApparelStyle.WomensTall)


class ApparelSize(base.PSBaseModel):
    apparelStyle: ApparelStyle
    labelSize: str
    customSize: str | None

    @model_validator(mode='before')
    @classmethod
    def fill_missing_label_size(cls, data):
        # Showdown Displays is sending empty labelSize
        label = data.get('labelSize')
        if not label or not str(label).strip():
            data['labelSize'] = '-'
            data['customSize'] = 'CUSTOM'
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
        return ''


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
    packageType: str
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

    def _get_colors(self) -> list[Color]:
        return self.ColorArray.Color if self.ColorArray else []

    def _set_colors(self, colors: list[Color]):
        self.ColorArray = ColorArray(Color=colors)

    Color = property(_get_colors, _set_colors)

    def get_size(self):
        apparel_size = self.ApparelSize
        if apparel_size:
            label_size = apparel_size.labelSize or ''
            if label_size.upper() == 'CUSTOM':
                return apparel_size.customSize
            return label_size
        return ''

    def get_primary_color(self):
        arr = self.ColorArray
        if arr:
            primary_color = arr.Color[0]
        else:
            primary_color = self.primaryColor
            if primary_color:
                primary_color = primary_color.Color
        return primary_color.colorName if primary_color else ''


class ProductPartArray(base.PSBaseModel):
    ProductPart: list[ProductPart]


class ProductPrice(base.PSBaseModel):
    quantityMax: int | None
    quantityMin: int
    price: Decimal
    discountCode: str | None


class ProductPriceArray(base.PSBaseModel):
    ProductPrice: list[ProductPrice]


class ProductPriceGroup(base.PSBaseModel):
    groupName: str
    currency: str
    description: str | None
    ProductPriceArray: ProductPriceArray

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
        return self.isCloseout or any(pp.isCloseout for pp in self.parts if pp.isCloseout)

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
            if variant['partId'] == part_id:
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
    discount = factors.get(discount_code, 0)
    ret = price * Decimal(1 - discount / 100)
    return ret.quantize(Decimal('.01'))
