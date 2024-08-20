import decimal
from datetime import datetime, date

from pydantic import Field

from .base import ServiceMessageArray, StrEnum, CountryIso2, Environment, PSBaseModel, Quantity, Currency

"""
The objects are defined based on https://tools.promostandards.org/purchase-order-1-0-0
"""


class OrderType(StrEnum):
    """
    “Blank”—This is data is for blank goods.

    “Sample”—This data is for a random sample order

    “Simple”—The data in the purchase order is sent over without supplier configured data and will be processed
    manually.

    “Configured”—The data is sent over in conjunction with the supplier’s Product Pricing and Configuration web service
    and designed for electronic processing of the purchase order.
    """
    Blank = "Blank"
    Sample = "Sample"
    Simple = "Simple"
    Configured = "Configured"


class DigitalProofType(StrEnum):
    """
    “Email”—The proof will be sent via email.

    “Webservice”—The proof will be sent via Webservice.
    """
    Email = "Email"
    Webservice = "Webservice"


class DigitalProofAddress(PSBaseModel):
    type: DigitalProofType
    email: str = Field(description="The address that the digital proof should be sent to prior to production")
    lineItemGroupingId: int = Field(description="What line item group does this proof address link to")


class DigitalProofAddressArray(PSBaseModel):
    DigitalProofAddress: list[DigitalProofAddress]


class DigitalProof(PSBaseModel):
    """
    An object containing preproduction digital proof information
    """
    required: bool
    DigitalProofAddressArray: DigitalProofAddressArray


class Program(PSBaseModel):
    """
    Program pricing information.
    """
    id: str
    name: str


class ToleranceType(StrEnum):
    """
    An enumerator specifying the quantity tolerance allowed:
    AllowOverRun, AllowUnderrun, AllowOverrunOrUnderrun, ExactOnly.

    Specifying AllowOverRun, AllowUnderrun or AllowOverrunOrUnderrun without a value and uom will result
    in the supplier’s discretion.
    """
    AllowOverRun = "AllowOverRun"
    AllowUnderrun = "AllowUnderrun"
    AllowOverrunOrUnderrun = "AllowOverrunOrUnderrun"
    ExactOnly = "ExactOnly"


class ToleranceUoM(StrEnum):
    """
    An enumerator specifying the unit of measure for the quantity tolerance allowed:
    Percent, Quantity.
    """
    Percent = "Percent"
    Quantity = "Quantity"


class ToleranceDetails(PSBaseModel):
    tolerance: ToleranceType
    value: decimal.Decimal
    # This element is ignored if ExactOnly is specified for tolerance.
    uom: ToleranceUoM


class GeometryType(StrEnum):
    Circle = "Circle"
    Rectangle = "Rectangle"
    Other = "Other"


class DimensionUoM(StrEnum):
    ACRE = "ACRE"
    ARES = "ARES"
    CELI = "CELI"
    CMET = "CMET"
    FOOT = "FOOT"
    GBGA = "GBGA"
    GBOU = "GBOU"
    GBPI = "GBPI"
    GBQA = "GBQA"
    GRAM = "GRAM"
    HECT = "HECT"
    INCH = "INCH"
    KILO = "KILO"
    KMET = "KMET"
    LITR = "LITR"
    METR = "METR"
    MILE = "MILE"
    MILI = "MILI"
    MMET = "MMET"
    PIEC = "PIEC"
    PUND = "PUND"
    SCMT = "SCMT"
    SMET = "SMET"
    SMIL = "SMIL"
    SQFO = "SQFO"
    SQIN = "SQIN"
    SQKI = "SQKI"
    SQMI = "SQMI"
    SQYA = "SQYA"
    TONS = "TONS"
    USGA = "USGA"
    USOU = "USOU"
    USPI = "USPI"
    USQA = "USGA"
    YARD = "YARD"


class Dimensions(PSBaseModel):
    """
    The dimensions of the artwork
    """
    geometry: GeometryType
    useMaxLocationDimensions: bool
    height: decimal.Decimal | None = None
    width: decimal.Decimal | None = None
    diameter: decimal.Decimal | None = None
    uom: DimensionUoM | None = None


class ContactDetails(PSBaseModel):
    attentionTo: str | None = None
    companyName: str | None = None
    address1: str | None = None
    address2: str | None = None
    address3: str | None = None
    city: str | None = None
    region: str | None = None
    postalCode: str | None = None
    country: CountryIso2 | None = None
    email: str | None = None
    phone: str | None = None
    comments: str | None = None


class ContactType(StrEnum):
    Art = "Art"
    Bill = "Bill"
    Expeditor = "Expeditor"
    Order = "Order"
    Sales = "Sales"
    Ship = "Ship"
    Sold = "Sold"


class Contact(PSBaseModel):
    contactType: ContactType
    ContactDetails: ContactDetails
    accountName: str | None
    accountNumber: str | None


class OrderContactArray(PSBaseModel):
    Contact: list[Contact]


class ThirdPartyAccount(PSBaseModel):
    """
    The third party account information for the shipping account to use and the business entity that is paying
    for the shipping
    """
    accountName: str
    accountNumber: str
    ContactDetails: ContactDetails


class ShipTo(PSBaseModel):
    customerPickup: bool
    shipmentId: int
    ContactDetails: ContactDetails


class FreightDetails(PSBaseModel):
    carrier: str = Field(description="The carrier name of the shipping vendor being requested. "
                                     "(i.e. “UPS”, “FEDEX”, etc.)")
    service: str = Field(description="The service code of the shipping vendor for the service being requested. "
                                     "i.e. GROUND, 2DAY, NEXTDAY, etc.")


class Shipment(PSBaseModel):
    # customerPickup: bool  # hit doesn't have this field here, but it's in the docs
    ShipTo: ShipTo
    packingListRequired: bool
    blindShip: bool
    allowConsolidation: bool
    FreightDetails: FreightDetails
    ThirdPartyAccount: ThirdPartyAccount | None
    shipReferences: list[str] | None = Field(description="Array of `two` strings max of identifiers used as the "
                                                         "reference fields used during the shipping process. "
                                                         "A shipReference can be a `purchase order number`, "
                                                         "`customer number`, `company name`, `Bill of Lading "
                                                         "number`, or a phrase that identifies that shipment",
                                             default=None)
    comments: str | None = None


class ShipmentArray(PSBaseModel):
    Shipment: list[Shipment]


class Typeset(PSBaseModel):
    sequenceNumber: int = Field(description="The order number of the typeset")
    value: str = Field(description="The typeset to be used on the order")
    font: str = Field(description="The font to use for the typeset")
    fontSize: decimal.Decimal = Field(description="The font size to use for the typeset")


class LayerOrStop(PSBaseModel):
    nameOrNumber: str = Field(description="The name or number of the layer or stop")
    description: str = Field(description="A human readable description of the layer")
    color: str = Field(description="The color value that corresponds to the colorSystem defined")


class LayerOrStopArray(PSBaseModel):
    LayerOrStop: list[LayerOrStop]


class ColorSystem(StrEnum):
    """
    Values are enumerated: Cmyk, Other, Pms, Rgb, Thread
    """
    Cmyk = "Cmyk"
    Other = "Other"
    Pms = "Pms"
    Rgb = "Rgb"
    Thread = "Thread"


class Layers(PSBaseModel):
    """
    An object that explains how the artwork layers or stops will be handled
    """
    colorSystem: ColorSystem
    LayerOrStopArray: LayerOrStopArray


class TransportMechanism(StrEnum):
    """
    The mechanism that will be used to transport the artwork; values are enumerated:
    “Email”, “Url”, “Ftp”, “ArtworkToFollow”
    """
    Email = "Email"
    Url = "Url"
    Ftp = "Ftp"
    ArtworkToFollow = "ArtworkToFollow"


class ArtworkType(StrEnum):
    """
    The purpose of the artwork file; values are enumerated:
    “ProductionReady”, “VirtualProof”, “SupplierArtTemplate”, “NonProductionReady”
    """
    ProductionReady = "ProductionReady"
    VirtualProof = "VirtualProof"
    SupplierArtTemplate = "SupplierArtTemplate"
    NonProductionReady = "NonProductionReady"


class ArtworkFile(PSBaseModel):
    fileName: str
    fileLocation: str
    transportMechanism: TransportMechanism = Field(examples=[TransportMechanism.Url])
    artworkType: ArtworkType


class ArtworkFileArray(PSBaseModel):
    ArtworkFile: list[ArtworkFile]


class Artwork(PSBaseModel):
    refArtworkId: str | None = Field(description="A pre-shared artwork Id that can be used by the supplier to find and "
                                                 "reference the artwork")
    description: str | None = Field(description="A textual description of the artwork being provided")
    Dimensions: Dimensions | None
    ArtworkFileArray: ArtworkFileArray | None
    instructions: str | None = Field(description="Any instructions regarding the processing or modification of artwork."
                                                 " `Adding instructions will cause delays in processing`")
    Layers: Layers | None
    TypesetArray: list[Typeset] | None
    totalStitchCount: int | None = Field(description="The total stitch count for the specified embroidery art")


class Decoration(PSBaseModel):
    decorationId: int = Field(description="The decorationId from the supplier’s PromoStandards Product Pricing and "
                                          "Configuration service",
                              examples=[58])
    decorationName: str | None = Field(description="The decorationName from the supplier’s PromoStandards Product "
                                                   "Pricing and Configuration service.",
                                       examples=["Color Print SilkScreen"])
    Artwork: Artwork


class DecorationArray(PSBaseModel):
    Decoration: list[Decoration]


class ChargeType(StrEnum):
    Freight = "Freight"
    Order = "Order"
    Run = "Run"
    Setup = "Setup"


class Charge(PSBaseModel):
    chargeId: str = Field(description="The chargeId from the supplier’s PromoStandards Product Pricing and "
                                      "Configuration service", max_length=64)
    chargeName: str | None
    description: str | None
    chargeType: ChargeType
    Quantity: Quantity
    unitPrice: decimal.Decimal | None
    extendedPrice: decimal.Decimal | None


class ChargeArray(PSBaseModel):
    """
    An array of charge information.

    This array should be populated with information from the supplier’s PromoStandards
    Product Pricing and Configuration service
    """
    Charge: list[Charge]


class ShipmentLink(PSBaseModel):
    shipmentId: int
    Quantity: Quantity


class ShipmentLinkArray(PSBaseModel):
    ShipmentLink: list[ShipmentLink]


class ReferenceNuberType(StrEnum):
    """
    The type of the prior order reference; values are enumerated: “PurchaseOrder”,”SalesOrder”, “JobOrWorkOrder”
    """
    PurchaseOrder = "PurchaseOrder"
    SalesOrder = "SalesOrder"
    JobOrWorkOrder = "JobOrWorkOrder"


class Location(PSBaseModel):
    locationLinkId: int = Field(description="An identifier to be used within the Part Array to link configured "
                                            "locations to a part.  Due to different colors and sizes, identical "
                                            "locations may need to be decorated differently",
                                examples=[1])
    locationId: int = Field(description="The locationId from the supplier’s PromoStandards Product Pricing and "
                                        "Configuration service", examples=[3174])
    locationName: str = Field(description="The locationName from the supplier’s PromoStandards Product Pricing and "
                                          "Configuration service", examples=["Left Chest"])
    DecorationArray: DecorationArray


class LocationArray(PSBaseModel):
    """
    An array of Decoration Location Information.

    This array should be populated with information from the supplier’s PromoStandards Product Pricing and
    Configuration service
    """
    Location: list[Location]


class Configuration(PSBaseModel):
    """
    An object containing line item configuration data
    """
    referenceNumber: str | None = Field(description="The previous order number that this purchase order is referencing")
    referenceNumberType: ReferenceNuberType | None = Field(description="The type of the prior order reference")
    preProductionProof: bool = Field(description="Indicates that this line item is for a pre-production proof")
    ChargeArray: ChargeArray | None
    LocationArray: LocationArray | None


class Part(PSBaseModel):
    partGroup: str | None = Field(description="An identifier that links common line item parts together")
    partId: str = Field(description="The part Id from the supplier’s PromoStandards Product Pricing and Configuration "
                                    "service")
    Quantity: Quantity
    customerPartId: str | None = Field(description="How the part is being represented to the distributor’s customer")
    customerSupplied: bool = Field(description="The part will be supplied by the customer or another entity other than "
                                               "the supplier")
    description: str | None = Field(description="The description from the supplier’s PromoStandards Product Pricing "
                                                "and Configuration service")
    locationLinkId: list[int] | None = Field(description="An array of location link Ids.  This links the part to its "
                                                         "configured locations")
    unitPrice: decimal.Decimal | None
    extendedPrice: decimal.Decimal | None
    ShipmentLinkArray: ShipmentLinkArray | None


class PartArray(PSBaseModel):
    Part: list[Part]


class LineType(StrEnum):
    """
    The type of order; values are enumerated:
·  “New” –A new purchase order with no prior order reference
·  “Repeat” —An exact repeat of a previous purchase order with the vendor
·  “Reference” –An order that has the same artwork as a previous order.
    """
    New = "New"
    Repeat = "Repeat"
    Reference = "Reference"


class LineItem(PSBaseModel):
    lineNumber: str
    description: str
    lineType: LineType
    Quantity: Quantity | None
    fobId: str | None = Field(description="Used to indicate the FOB point.  Use fobId from the supplier’s Product "
                                          "Pricing and Configuration Service to populate this information",
                              default=None)
    ToleranceDetails: ToleranceDetails
    allowPartialShipments: bool
    unitPrice: decimal.Decimal | None
    lineItemTotal: decimal.Decimal
    requestedShipDate: date | None = Field(description="The date the line item is requested to ship from the FOB point")
    requestedInHandsDate: date | None = Field(description="The date the line item is requested to arrive at the "
                                                          "shipping destination")
    referenceSalesQuote: str | None = Field(description="The sales quote number associated with this purchase order "
                                                        "line (if applicable)")
    Program: Program | None
    endCustomerSalesOrder: str | None = Field(description="The distributor’s order number provided to the end customer")
    productId: str | None = Field(description="The manufacturer’s product id associated with the configuration data")
    customerProductId: str | None = Field(description="The distributor’s product id")
    lineItemGroupingId: int | None = Field(description="An identifier that allows configuration data to be spread out "
                                                       "among multiple purchase order lines. Keep `lineItemGroupingID` "
                                                       "unique when referencing the same product on the purchase order."
                                                       "  Any change to the product, location, decoration, or artwork "
                                                       "should produce a unique `lineItemGroupingID` to the purchase "
                                                       "order")
    PartArray: PartArray | None
    Configuration: Configuration | None


class LineItemArray(PSBaseModel):
    LineItem: list[LineItem]


class TaxType(StrEnum):
    HST_GST = "Hst-Gst"
    PST = "Pst"
    SALES_TAX = "SalesTax"


class TexInformation(PSBaseModel):
    taxId: str = Field(description="The purchasers tax identifier")
    taxType: TaxType
    taxExempt: bool
    taxJurisdiction: list[str]
    taxAmount: decimal.Decimal | None = Field(description="The amount of tax for this purchase order")


class TaxInformationArray(PSBaseModel):
    TaxInformation: list[TexInformation]


class PO(PSBaseModel):
    environment: Environment | None = Field(description="The environment the purchase order is being sent from. "
                                                        "Should be STAGING or PROD", examples=["STAGING"],
                                            default=Environment.PROD,
                                            title='environment')
    orderType: OrderType
    orderNumber: str
    orderDate: datetime
    lastModified: datetime | None
    totalAmount: decimal.Decimal = Field(description="The total amount of the purchase order")
    paymentTerms: str = Field(description="ie. NET15, NET30, etc.", examples=["NET30"])
    rush: bool = Field(default=False, description="Used to indicate a rush on the purchase order")
    currency: Currency = Field(description="The currency the purchase order is transacted in ISO4217 format."
                                           " ie. USD, CAD, EUR, JPY, GBP, etc.", examples=["USD"])
    DigitalProof: DigitalProof | None
    OrderContactArray: OrderContactArray | None
    ShipmentArray: ShipmentArray
    LineItemArray: LineItemArray
    termsAndConditions: str = Field(description="The terms and conditions of the purchase order",
                                    examples=["terms agreed to"])
    salesChannel: str | None = Field(description="The sales channel the purchase order",
                                     examples=["SHOPIFYAPP"])
    promoCode: str | None = Field(default=None, examples=["SUMMER2023"])
    TaxInformationArray: TaxInformationArray | None


class SupportedOrderType(StrEnum):
    """
    The type of order; values are enumerated: “Blank”, “Sample”, “Simple” “Configured”
    """
    Blank = "Blank"
    Sample = "Sample"
    Simple = "Simple"
    Configured = "Configured"


class GetSupportedOrderTypesResponse(PSBaseModel):
    """
    Response to a getSupportedOrderTypes method.
    """
    supportedOrderTypes: list[SupportedOrderType] | None
    ServiceMessageArray: ServiceMessageArray | None


class SendPOResponse(PSBaseModel):
    """
    Response to a sendPO method.
    """
    transactionId: str | None
    ServiceMessageArray: ServiceMessageArray | None
