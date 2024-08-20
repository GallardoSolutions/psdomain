import typing
from datetime import datetime
from decimal import Decimal

from .. import base
from ..base import StrEnum


class ProductCategory(base.PSBaseModel):
    category: str | None
    subCategory: str | None


class ProductCategoryArray(base.PSBaseModel):
    ProductCategory: list[ProductCategory]


class RelatedProduct(base.PSBaseModel):
    relationType: str
    productId: str
    partId: str | None


class RelatedProductArray(base.PSBaseModel):
    RelatedProduct: list[RelatedProduct]


class ApparelSize(base.PSBaseModel):
    apparelStyle: str
    labelSize: str
    customSize: str | None


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
    colorName: str
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
    SpecificationUom: str
    measurementValue: str | None


class SpecificationArray(base.PSBaseModel):
    Specification: list[Specification]


class ProductPart(base.PSBaseModel):
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
    primaryColor: PrimaryColor | None = None   # in V1 is not required
    ColorArray: ColorArray | None
    ProductPackagingArray: ProductPackagingArray | None
    ShippingPackageArray: ShippingPackageArray | None

    def _get_colors(self) -> list[Color]:
        return self.ColorArray.Color if self.ColorArray else []

    def _set_colors(self, colors: list[Color]):
        self.ColorArray = ColorArray(Color=colors)

    Color = property(_get_colors, _set_colors)


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


class ProductPriceGroupArray(base.PSBaseModel):
    ProductPriceGroup: list[ProductPriceGroup]


class ProductKeyword(base.PSBaseModel):
    keyword: str


class ProductKeywordArray(base.PSBaseModel):
    ProductKeyword: list[ProductKeyword]


class LocationDecoration(base.PSBaseModel):
    locationName: str
    maxImprintColors: int | None
    decorationName: str
    locationDecorationComboDefault: bool
    priceIncludes: bool


class LocationDecorationArray(base.PSBaseModel):
    LocationDecoration: list[LocationDecoration]


class FobPoint(base.PSBaseModel):
    fobId: str
    fobPostalCode: str
    fobCity: str
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
    ProductMarketingPointArray:  typing.Optional[ProductMarketingPointArray] | None

    @property
    def available_colors(self) -> list[Color]:
        colors_list = []

        for part in self.ProductPartArray.ProductPart:
            if part.ColorArray and part.ColorArray.Color:
                colors = part.ColorArray.Color
                for color in colors:
                    color_name = color.colorName
                    if color_name not in colors_list:
                        colors_list.append(color)
        return colors_list

    @property
    def sizes(self) -> list[str]:
        sizes_list = []

        for part in self.ProductPartArray.ProductPart:
            if part.ApparelSize:
                size_name = part.ApparelSize.labelSize
                if size_name not in sizes_list:
                    sizes_list.append(size_name)

        return sizes_list


class Location(base.PSBaseModel):
    locationId: int
    locationName: str


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
