from datetime import datetime
from decimal import Decimal

from pydantic import Field, model_validator

from .product_data import common as product_data
from . import base
from .countries import normalize_country


def normalize_uom(values, field_name):
    if field_name in values:
        try:
            if values[field_name]:
                val = values[field_name].capitalize()
                if val in ['Square inches', 'Squareinches']:
                    values[field_name] = DecorationUomType.SQUARE_INCHES
                elif val == 'Inch':
                    values[field_name] = DecorationUomType.INCHES
                else:
                    values[field_name] = DecorationUomType(val)
        except ValueError:
            raise ValueError(f"Invalid {field_name} value: {values[field_name]}")
    return values


def normalize_charge_type(values, field_name):
    if field_name in values:
        try:
            if values[field_name]:
                val = values[field_name].capitalize()
                if val == 'Tape setup':
                    values[field_name] = ChargeType.SETUP
                else:
                    values[field_name] = ChargeType(val)
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


class DecorationColorResponse(base.ErrorMessageResponse):
    DecorationColors: DecorationColors | None

    @property
    def colors(self):
        temp = self.DecorationColors
        return temp.ColorArray.Color if temp and temp.ColorArray else []

    @property
    def decoration_methods(self):
        temp = self.DecorationColors
        return temp.DecorationMethodArray.DecorationMethod if temp and temp.DecorationMethodArray else []


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
    fobPostalCode: str | None
    fobCity: str | None
    fobState: str | None
    fobCountry: str | None
    CurrencySupportedArray: CurrencySupportedArray | None  # HIT error
    ProductArray: ProductArray | None  # Spector error

    @model_validator(mode='before')
    def normalize_dob_country(cls, values):
        return normalize_country(values, 'fobCountry')

    def __str__(self):
        fob_id = f'{self.fobId[:10]}...' if self.fobId and len(self.fobId) > 10 else self.fobId
        return f"{fob_id} at {self.fobPostalCode} {self.fobCity}-{self.fobState}({self.fobCountry})"

    @property
    def products(self):
        lst = self.ProductArray.Product if self.ProductArray else []
        return [p.productId for p in lst]

    @property
    def currencies(self):
        lst = self.CurrencySupportedArray.CurrencySupported if self.CurrencySupportedArray else []
        return [c.currency for c in lst]


class FobPointArray(base.PSBaseModel):
    FobPoint: list[FobPoint]


class FobPointsResponse(base.ErrorMessageResponse):
    FobPointArray: FobPointArray | None

    @property
    def fob_points(self):
        return self.FobPointArray.FobPoint if self.FobPointArray else []

    @property
    def fob_point_ids(self):
        return [fp.fobId for fp in self.fob_points]

    @property
    def currencies(self):
        ret = set()
        for fp in self.fob_points:
            ret.update(fp.currencies)
        return ret


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
    price: Decimal
    discountCode: str | None = Field(description='The industry discount code associated with the price')
    repeatPrice: Decimal | None
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

    @property
    def is_run(self) -> bool:
        return self.chargeType.is_run

    @property
    def is_setup(self) -> bool:
        return self.chargeType.is_setup

    @property
    def is_order(self) -> bool:
        return self.chargeType.is_order

    @property
    def prices(self) -> list[ChargePrice]:
        # returns a sorted list of part prices by minQuantity if PartPriceArray is not None, empty list otherwise
        result = getattr(self, '_prices', None)
        if result is None:
            result = sorted(self.ChargePriceArray.ChargePrice, key=lambda p: p.xMinQty) if self.ChargePriceArray else []
            setattr(self, '_prices', result)
        return result

    @property
    def x_min_qty(self) -> int | None:
        prices = self.prices
        return prices[0].xMinQty if prices else None

    @property
    def y_min_qty(self) -> int | None:
        prices = self.prices
        return prices[0].yMinQty if prices else None

    @property
    def reversed_prices(self) -> list[ChargePrice]:
        return self.prices[::-1]

    def get_price(self, qty: int) -> ChargePrice | None:
        # returns the price for the given quantity if it exists, None otherwise
        for ch in self.reversed_prices:
            if ch.xMinQty <= qty:
                return ch
        return None

    def get_charge_price(self, qty: int, repeat_price: bool, num_colors: int = 1) -> Decimal | None:
        ch = self.get_price(qty)
        if ch:
            unit_price = ch.repeatPrice if repeat_price else ch.price
            charges_per_color = self.chargesPerColor or 1
            if charges_per_color > 1:
                # todo: implement this logic
                unit_price = unit_price + charges_per_color
            return unit_price
        return None

    @property
    def is_extra_color(self) -> bool:
        return (self.chargesPerColor and self.chargesPerColor > 1) or 'extra color' in self.chargeName.lower()

    @property
    def is_extra_location(self) -> bool:
        return self.chargesPerLocation and self.chargesPerLocation > 1 or 'extra location' in self.chargeName.lower()

    @property
    def is_extra_stitch(self) -> bool:
        return 'extra stitch' in self.chargeName.lower()

    @property
    def is_ltm(self) -> bool:
        return self.chargesAppliesLTM

    @model_validator(mode='before')
    def normalize_charge_type(cls, values):
        return normalize_charge_type(values, 'chargeType')


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
    decorationHeight: Decimal | None = Field(examples=['4.0'])
    decorationWidth: Decimal | None = Field(examples=['7.0'])
    decorationDiameter: Decimal | None
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

    @property
    def charges(self):
        return self.ChargeArray.Charge if self.ChargeArray else []

    def has_extra_color_charge(self):
        return any(ch for ch in self.charges if ch.is_extra_color)

    def has_extra_location_charge(self):
        return any(ch for ch in self.charges if ch.is_extra_location)

    def has_extra_stitch_charge(self):
        return any(ch for ch in self.charges if ch.is_extra_stitch)

    def get_set_up_price(self, decorations_included: int, qty: int, qty_dec: int,
                         dec_uom: DecorationUomType, no_locs: int, repeat: bool = False) -> Decimal | None:
        """
        :param decorations_included: how many decorations are included in the price
        :param qty: amount of units ordered
        :param qty_dec: how many decorations are ordered
        :param dec_uom: decorations unit of measure
        :param no_locs: number of locations
        :param repeat: is already a repeat order
        :return: setup price if it exists, None otherwise
        """
        assert dec_uom == self.decorationUom
        if self.itemPartQuantityLTM:
            assert qty_dec >= self.itemPartQuantityLTM
        for charge in self.charges:
            if charge.is_setup:
                ret = charge.get_charge_price(qty, repeat, qty_dec)
                if no_locs > 1:
                    ret *= no_locs
                return ret

    def get_run_price(self, decorations_included: int, qty: int, qty_dec: int,
                      dec_uom: DecorationUomType, no_locs: int, repeat: bool = False):
        """
        :param decorations_included: how many decorations are included in the price
        :param qty: amount of units ordered
        :param qty_dec: how many decorations are ordered
        :param dec_uom: decorations unit of measure
        :param no_locs: number of locations
        :param repeat: is already a repeat order
        :return: run charge if it exists, None otherwise
        """
        assert dec_uom == self.decorationUom
        if self.itemPartQuantityLTM:
            assert qty_dec >= self.itemPartQuantityLTM
        for charge in self.charges:
            if charge.is_run:
                # todo: add ChargesPerLocation and ChargesPerColor logic
                new_qty_dec = qty_dec - decorations_included if decorations_included else qty_dec
                ret = charge.get_charge_price(qty, repeat, new_qty_dec)
                if no_locs > 1:
                    other_locs_price = charge.get_charge_price(qty, repeat, qty_dec)
                    ret + other_locs_price * (no_locs - 1)
                return ret


class DecorationArray(base.PSBaseModel):
    Decoration: list[Decoration]


class Location(base.PSBaseModel):
    locationId: int
    locationName: str
    DecorationArray: DecorationArray | None
    decorationsIncluded: int
    defaultLocation: bool
    maxDecoration: int
    minDecoration: int
    locationRank: int | None = Field(description='Popularity of location based on supplier experience')

    @property
    def decorations(self):
        return self.DecorationArray.Decoration if self.DecorationArray else []

    def get_prices(self, method: int, qty: int, qty_dec: int, dec_uom: DecorationUomType,
                   no_locs: int = 1, repeat=False) -> (Decimal | None, Decimal | None):
        # returns setup price, run charge for the given quantity if it exists, None otherwise
        assert qty >= 0
        assert qty_dec >= self.minDecoration
        assert qty_dec < self.maxDecoration
        assert no_locs >= 1

        for decoration in self.decorations:
            if decoration.decorationId != method:
                continue
            setup_price = decoration.get_set_up_price(self.decorationsIncluded, qty, qty_dec, dec_uom, no_locs, repeat)
            run_price = decoration.get_run_price(self.decorationsIncluded, qty, qty_dec, dec_uom, no_locs, repeat)
            return setup_price, run_price
        return None, None


class LocationArray(base.PSBaseModel):
    Location: list[Location]


class AvailableLocationArray(base.PSBaseModel):
    AvailableLocation: list[product_data.Location]


class AvailableLocationsResponse(base.ErrorMessageResponse):
    AvailableLocationArray: AvailableLocationArray | None

    @property
    def locations(self):
        arr = self.AvailableLocationArray.AvailableLocation if self.AvailableLocationArray else []
        return arr


class AvailableCharge(base.PSBaseModel):
    chargeId: int
    chargeName: str
    chargeType: ChargeType
    chargeDescription: str | None

    @model_validator(mode='before')
    def normalize_charge_type(cls, values):
        return normalize_charge_type(values, 'chargeType')


class AvailableChargeArray(base.PSBaseModel):
    AvailableCharge: list[AvailableCharge]


class AvailableChargesResponse(base.ErrorMessageResponse):
    AvailableChargeArray: AvailableChargeArray | None

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
    price: Decimal = Field(description='The base price of the good without decoration')
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
    ratio: Decimal = Field(description='Describes how the amount of partIds that need to be added to the order '
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

    @property
    def location_ids(self) -> list[str | int]:
        return [x.locationId for x in self.LocationIdArray.LocationId] if self.LocationIdArray else []


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

    @property
    def parts(self):
        return self.PartArray.Part if self.PartArray else []

    @property
    def fob_points(self):
        return self.FobArray.Fob if self.FobArray else []


class ConfigurationAndPricingResponse(base.ErrorMessageResponse):
    Configuration: Configuration | None

    @property
    def locations(self):
        return self.Configuration.locations if self.Configuration else []

    @property
    def parts(self):
        return self.Configuration.parts if self.Configuration else []

    @property
    def fob_points(self):
        return self.Configuration.fob_points if self.Configuration else []
