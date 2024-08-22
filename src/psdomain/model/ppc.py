import decimal
from datetime import datetime

from pydantic import Field, model_validator

from .product_data import common as product_data
from . import base


def normalize_uom(values, field_name):
    if field_name in values:
        try:
            if values[field_name] == 'SQUARE INCHES':
                values[field_name] = DecorationUomType.SQUARE_INCHES
            elif values[field_name]:
                values[field_name] = DecorationUomType(values[field_name].capitalize())
        except ValueError:
            raise ValueError(f"Invalid {field_name} value: {values[field_name]}")
    return values


class ChargeType(base.StrEnum):
    """
    Types of Charges
    """
    SETUP = "Setup"
    RUN = "Run"
    ORDER = "Order"

    @property
    def is_run(self) -> bool:
        return self == ChargeType.RUN

    @property
    def is_setup(self) -> bool:
        return self == ChargeType.SETUP

    @property
    def is_order(self) -> bool:
        return self == ChargeType.ORDER


class ColorArray(base.PSBaseModel):
    Color: list[product_data.Color]


class DecorationMethod(base.PSBaseModel):
    decorationId: int
    decorationName: str


class DecorationMethodArray(base.PSBaseModel):
    DecorationMethod: list[DecorationMethod]


class DecorationColors(base.PSBaseModel):
    productId: str
    locationId: int
    pmsMatch: bool
    fullColor: bool = Field(description="Set to true if the decoration method is full color process; False implies "
                                        "that number of colors is irrelevant")
    ColorArray: ColorArray | None  # the docs say this is required, but HIT does not have it
    DecorationMethodArray: DecorationMethodArray | None  # # the docs say this is required but not sure


class DecorationColorResponse(base.PSBaseModel):
    DecorationColors: DecorationColors | None
    ErrorMessage: base.ErrorMessage | None

    @property
    def if_ok(self):
        return self.ErrorMessage is None


class Product(base.PSBaseModel):
    productId: str


class ProductArray(base.PSBaseModel):
    Product: list[Product]


class CurrencySupported(base.PSBaseModel):
    currency: base.Currency

    def __hash__(self):
        return hash(self.currency)


class CurrencySupportedArray(base.PSBaseModel):
    CurrencySupported: list[CurrencySupported]


class FobPoint(base.PSBaseModel):
    fobId: str
    fobPostalCode: str
    fobCity: str
    fobState: str
    fobCountry: str
    CurrencySupportedArray: CurrencySupportedArray | None  # HIT error
    ProductArray: ProductArray | None  # Spector error

    def __str__(self):
        fob_id = f'{self.fobId[:10]}...' if self.fobId and len(self.fobId) > 10 else self.fobId
        return f"{fob_id} at {self.fobPostalCode} {self.fobCity}-{self.fobState}({self.fobCountry})"


class FobPointArray(base.PSBaseModel):
    FobPoint: list[FobPoint]


class FobPointsResponse(base.PSBaseModel):
    FobPointArray: FobPointArray | None
    ErrorMessage: base.ErrorMessage | None

    @property
    def if_ok(self):
        return self.ErrorMessage is None


class DecorationUomType(base.StrEnum):
    COLORS = "Colors"
    INCHES = "Inches"
    OTHER = "Other"
    STITCHES = "Stitches"
    SQUARE_INCHES = "SquareInches"
    LOCATIONS = "Locations"  # Gemline added this one in their response


class ChargePrice(base.PSBaseModel):
    xMinQty: int
    xUom: base.UOM = Field(examples=['EA'])
    yMinQty: int
    yUom: DecorationUomType = Field(examples=['Colors'])
    price: decimal.Decimal
    discountCode: str | None = Field(description='The industry discount code associated with the price')
    repeatPrice: decimal.Decimal | None
    repeatDiscountCode: str | None
    priceEffectiveDate: datetime | None
    priceExpiryDate: datetime | None

    @model_validator(mode='before')
    def normalize_y_uom(cls, values):
        return normalize_uom(values, 'yUom')


class ChargePriceArray(base.PSBaseModel):
    ChargePrice: list[ChargePrice]


class Charge(base.PSBaseModel):
    chargeId: int
    chargeName: str
    chargeType: ChargeType
    chargeDescription: str
    ChargePriceArray: ChargePriceArray | None  # TerryTown is sending None although the docs say it is required
    chargesAppliesLTM: bool | None = Field(description='This charge is applied with ordering Less than Minimum (LTM)',
                                           default=False)
    chargesPerLocation: int | None = Field(description='The number of times a charge will occur per location')
    chargesPerColor: int | None = Field(description='The number of times a charge will occur per color')


class ChargeArray(base.PSBaseModel):
    Charge: list[Charge]


class DecorationGeometryType(base.StrEnum):
    """
    Decoration Geometry Types
    """
    CIRCLE = "Circle"
    RECTANGLE = "Rectangle"
    OTHER = "Other"


class Decoration(base.PSBaseModel):
    decorationId: int
    decorationName: str
    decorationGeometry: DecorationGeometryType = Field(examples=['Rectangle'])
    decorationHeight: decimal.Decimal | None = Field(examples=['4.0'])
    decorationWidth: decimal.Decimal | None = Field(examples=['7.0'])
    decorationDiameter: decimal.Decimal | None
    decorationUom: DecorationUomType = Field(description='The unit of measure for the decoration area',
                                             examples=['Inches'])
    allowSubForDefaultLocation: bool | None = Field(description='Buyer is allowed to substitute a decoration location '
                                                                'without changing the price')
    allowSubForDefaultMethod: bool | None = Field(description='Buyer is allowed to substitute this decoration method '
                                                              'without changing the price')
    itemPartQuantityLTM: int | None = Field('Specifies the Part Quantity that is the absolute minimum that can be '
                                            'ordered with a Less Than Minimum (LTM) charge')
    ChargeArray: ChargeArray | None
    decorationUnitsIncluded: int | None = Field(description='The number of included decoration units. For example, '
                                                            'if 1 color decoration is included set value to “1”. '
                                                            'If 7,500 stitches are included set value to “7500”')
    decorationUnitsIncludedUom: DecorationUomType | None
    decorationUnitsMax: int | None = Field(description='This is the max number of decoration units for this '
                                                       'decoration/location combination.',
                                           examples=[4])
    defaultDecoration: bool | None = Field(description='Specifies whether this is the default decoration '
                                                       'for this location')
    leadTime: int | None = Field(description='The lead time for the given decoration', examples=[7])
    rushLeadTime: int | None = Field(description='The lead time for rush service for a given decoration '
                                                 '(rush charges may apply)', examples=[3])

    @model_validator(mode='before')
    def normalize_decoration_units_include_uom(cls, values):
        return normalize_uom(values, 'decorationUnitsIncludedUom')

    @model_validator(mode='before')
    def normalize_decoration_uom(cls, values):
        return normalize_uom(values, 'decorationUom')


class DecorationArray(base.PSBaseModel):
    Decoration: list[Decoration]


class Location(base.PSBaseModel):
    locationId: int
    locationName: str
    DecorationArray: DecorationArray
    decorationsIncluded: int
    defaultLocation: bool
    maxDecoration: int
    minDecoration: int
    locationRank: int | None = Field(description='Popularity of location based on supplier experience')


class LocationArray(base.PSBaseModel):
    Location: list[Location]


class AvailableLocationArray(base.PSBaseModel):
    AvailableLocation: list[product_data.Location]


class AvailableLocationsResponse(base.PSBaseModel):
    AvailableLocationArray: AvailableLocationArray | None
    ErrorMessage: base.ErrorMessage | None

    @property
    def if_ok(self):
        return self.ErrorMessage is None

    @property
    def locations(self):
        arr = self.AvailableLocationArray.AvailableLocation if self.AvailableLocationArray else []
        return arr


class AvailableCharge(base.PSBaseModel):
    chargeId: int
    chargeName: str
    chargeType: ChargeType
    chargeDescription: str | None


class AvailableChargeArray(base.PSBaseModel):
    AvailableCharge: list[AvailableCharge]


class AvailableChargesResponse(base.PSBaseModel):
    AvailableChargeArray: AvailableChargeArray | None
    ErrorMessage: base.ErrorMessage | None = None

    @property
    def if_ok(self):
        return self.ErrorMessage is None

    @property
    def charges(self):
        arr = self.AvailableChargeArray.AvailableCharge if self.AvailableChargeArray else []
        return arr


class LocationId(base.PSBaseModel):
    locationId: str | int


class LocationIdArray(base.PSBaseModel):
    LocationId: list[LocationId]


class PartPrice(base.PSBaseModel):
    minQuantity: int = Field(description='The minimum quantity for the price')
    discountCode: str | None = Field(description='The industry discount code associated with the price.')
    price: decimal.Decimal = Field(description='The base price of the good without decoration')
    priceUom: base.UOM = Field(examples=['EA'], description='The unit of measure for the price')
    priceEffectiveDate: datetime | None  # StormCreek is returning None for this field
    priceExpiryDate: datetime | None  # Spector is returning None for this field

    def __le__(self, other):
        return self.minQuantity <= other.minQuantity


class PartPriceArray(base.PSBaseModel):
    PartPrice: list[PartPrice]


class Part(base.PSBaseModel):
    partId: str
    partDescription: str | None
    PartPriceArray: PartPriceArray | None
    partGroup: int = Field(description='A numeric identifier grouping mutually exclusive parts together. When '
                                       'configuring data, always start with part group “1”',
                           examples=[1])
    nextPartGroup: int | None = Field(description='The next mutually exclusive partGroup to complete configuration of'
                                                  'the product', default=None)
    partGroupRequired: bool = Field(description='A boolean value specifying if this partGroup is required for the '
                                                'product configuration. If set to TRUE, a selection in the partGroup '
                                                'is required for ordering')
    partGroupDescription: str = Field(description='A description of the partGroup: Optional Lid`, `Straw',
                                      examples=['Main Product', 'Optional Lid', 'Straw'])
    ratio: decimal.Decimal = Field(description='Describes how the amount of partIds that need to be added to the order '
                                               'based on the number of products ordered',
                                   examples=[
                                       'If 8 partIds would be required per 1 product ordered, then 8 should be '
                                       'used as the ratio. If one partId is required for every 8 products, than '
                                       'use .125'])
    defaultPart: bool | None = Field(description='This part is included in the “Basic Pricing Configuration” service '
                                                 'price. This field is optional, but highly encouraged')
    LocationIdArray: LocationIdArray | None

    @property
    def prices(self) -> list[PartPrice]:
        # returns a sorted list of part prices by minQuantity if PartPriceArray is not None, empty list otherwise
        return sorted(self.PartPriceArray.PartPrice, key=lambda p: p.minQuantity) if self.PartPriceArray else []

    def get_price(self, qty: int) -> PartPrice | None:
        # returns the price for the given quantity if it exists, None otherwise
        reversed_prices = self.prices[::-1]
        for price in reversed_prices:
            if price.minQuantity <= qty:
                return price
        return None


class PartArray(base.PSBaseModel):
    Part: list[Part]


class Configuration(base.PSBaseModel):
    PartArray: PartArray | None
    LocationArray: LocationArray | None
    productId: str | None = None
    currency: str
    FobArray: base.FobArray | None
    fobPostalCode: str | None = None
    priceType: base.PriceType

    @property
    def locations(self):
        return self.LocationArray.Location if self.LocationArray else []


class ConfigurationAndPricingResponse(base.PSBaseModel):
    Configuration: Configuration | None
    ErrorMessage: base.ErrorMessage | None

    @property
    def if_ok(self):
        return self.ErrorMessage is None
