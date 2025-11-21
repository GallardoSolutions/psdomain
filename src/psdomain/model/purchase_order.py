import decimal
from datetime import datetime, date
from typing import Annotated

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
    geometry: GeometryType = Field(description="The geometry of the decoration",
                                   examples=['Rectangle', 'Circle', 'Other'])
    useMaxLocationDimensions: bool = Field(
        description="Use the maximum allowed imprint dimensions for this location. If this is set to true, all other "
                    "dimension information is ignored except for geometry.")
    height: decimal.Decimal | None = Field(
        description="The height of the artwork; leave blank if the imprint is not rectangular.",
        default=None)
    width: decimal.Decimal | None = Field(
        description="The width of artwork; leave blank if the imprint is not rectangular.",
        default=None
    )
    diameter: decimal.Decimal | None = Field(
        description="The diameter of the artwork; leave blank if the imprint is not circular.",
        default=None
    )
    uom: DimensionUoM | None = Field(description="The unit of measure for the decoration area in ISO 20022.",
                                     default=None)


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
    comments: str | None = Field(
        description="Comments regarding the contact for further clarification. Note: Use comments only when "
                    "absolutely necessary, as it may cause delays in order processing.",
        default=None
    )


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
    ContactDetails: Annotated[
        ContactDetails,
        Field(description="The object that contains the details about the contact.", )
    ]
    accountName: str | None = Field(
        description="The name of the account that will be invoiced for the purchase order. Should be populated when "
                    "the contactType is Bill.",
        default=None)
    accountNumber: str | None = Field(
        description="The number of the account that will be invoiced for the purchase order. Should be populated when "
                    "the contactType is Bill.",
        default=None
    )


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
    ShipTo: Annotated[
        ShipTo,
        Field(description="The object containing the ship to information")
    ]

    packingListRequired: bool = Field(description="Packing list required.")
    blindShip: bool = Field(description="Require blind shipping.")
    allowConsolidation: bool = Field(description="Allow consolidation of shipments.")

    FreightDetails: Annotated[
        FreightDetails,
        Field(description="Freight: carrier and service details.")
    ]

    ThirdPartyAccount: Annotated[
        ThirdPartyAccount | None,
        Field(
            description="The object containing the third party information for the shipping account to use and the "
                        "business entity that is paying for the shipping. Known as ship using this account.",
            default=None
        )
    ]

    shipReferences: list[str] | None = Field(description="Array of `two` strings max of identifiers used as the "
                                                         "reference fields used during the shipping process. "
                                                         "A shipReference can be a `purchase order number`, "
                                                         "`customer number`, `company name`, `Bill of Lading "
                                                         "number`, or a phrase that identifies that shipment",
                                             default=None)

    comments: str | None = Field(
        description="Comments regarding the shipment for further clarification. Note: Use comments only when "
                    "necessary, as it may cause delays in order processing.",
        default=None
    )


class ShipmentArray(PSBaseModel):
    Shipment: list[Shipment]


class Typeset(PSBaseModel):
    sequenceNumber: int = Field(description="The order number of the typeset")
    value: str = Field(description="The typeset to be used on the order")
    font: str | None = Field(description="The font to use for the typeset", default=None)
    fontSize: decimal.Decimal | None = Field(description="The font size to use for the typeset",
                                             default=None)


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
                                                 "reference the artwork",
                                     default=None)
    description: str | None = Field(description="A textual description of the artwork being provided",
                                    default=None)
    Dimensions: Dimensions | None = Field(description="Dimensions of the artwork being provided",
                                          default=None)
    ArtworkFileArray: ArtworkFileArray | None = Field(description="An array of artwork file data.",
                                                      default=None)
    instructions: str | None = Field(description="Any instructions regarding the processing or modification of artwork."
                                                 " `Adding instructions will cause delays in processing`",
                                     default=None)
    Layers: Layers | None = Field(description="An object that explains how the artwork layers or "
                                              "stops will be handled.", default=None)
    TypesetArray: list[Typeset] | None = Field(description="An array of typeset data.", default=None)
    totalStitchCount: int | None = Field(description="The total stitch count for the specified embroidery art",
                                         default=None)


class Decoration(PSBaseModel):
    decorationId: int = Field(description="The decorationId from the supplier’s PromoStandards Product Pricing and "
                                          "Configuration service",
                              examples=[58])
    decorationName: str | None = Field(description="The decorationName from the supplier’s PromoStandards Product "
                                                   "Pricing and Configuration service.",
                                       examples=["Color Print SilkScreen"],
                                       default=None)
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
    chargeName: str | None = Field(
        description="The chargeName from the supplier’s PromoStandards Product Pricing and Configuration service.",
        default=None
    )
    description: str | None = Field(
        description="The charge description from the supplier’s PromoStandards Product Pricing and "
                    "Configuration service.",
        default=None
    )
    chargeType: ChargeType
    Quantity: Quantity
    unitPrice: decimal.Decimal | None = Field(description="The price of the charge being referenced.",
                                              default=None)
    extendedPrice: decimal.Decimal | None = Field(description="The unitPrice multiplied by the Quantity value.",
                                                  default=None)


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
    locationName: str | None = Field(
        description="The locationName from the supplier’s PromoStandards Product Pricing and "
                    "Configuration service", examples=["Left Chest"],
        default=None)
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
    ChargeArray: ChargeArray | None = Field(
        description="An array of product part information. This array should be populated with information from the "
                    "supplier’s PromoStandards Product Pricing and Configuration service",
        default=None)
    LocationArray: LocationArray | None = Field(
        description="An array of Decoration Location Information. This array should be populated with information "
                    "from the supplier’s PromoStandards Product Pricing and Configuration service",
        default=None)


class Part(PSBaseModel):
    partGroup: str | None = Field(description="An identifier that links common line item parts together",
                                  default=None)
    partId: str = Field(description="The part Id from the supplier’s PromoStandards Product Pricing and Configuration "
                                    "service")
    Quantity: Quantity
    customerPartId: str | None = Field(description="How the part is being represented to the distributor’s customer",
                                       default=None)
    customerSupplied: bool = Field(description="The part will be supplied by the customer or another entity other than "
                                               "the supplier")
    description: str | None = Field(description="The description from the supplier’s PromoStandards Product Pricing "
                                                "and Configuration service",
                                    default=None)
    locationLinkId: list[int] | None = Field(description="An array of location link Ids.  This links the part to its "
                                                         "configured locations",
                                             default=None)
    unitPrice: decimal.Decimal | None = Field(description="The price of the part being referenced.", default=None)
    extendedPrice: decimal.Decimal | None = Field(description="The unitPrice multiplied by the Quantity value.",
                                                  default=None)
    ShipmentLinkArray: ShipmentLinkArray | None = Field(
        description="Link this part and a specified quantity to one or many shipments.",
        default=None
    )


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
    lineNumber: str = Field(description="The line number of the line item")
    description: str = Field(
        description="The description of the line item. For simple order type (not using a configuration), use this "
                    "field to explain the details.")
    lineType: LineType = Field(
        description='The type of order; values are enumerated: '
                    '“New” –A new purchase order with no prior order reference, '
                    '“Repeat” —An exact repeat of a previous purchase order with the vendor, '
                    '“Reference” –An order that has the same artwork as a previous order.',
    )
    Quantity: Quantity | None = Field(description="The quantity object that contains the value and unit of measure.",
                                      default=None)
    fobId: str | None = Field(description="Used to indicate the FOB point.  Use fobId from the supplier’s Product "
                                          "Pricing and Configuration Service to populate this information",
                              default=None)
    ToleranceDetails: ToleranceDetails = Field(
        description="The object containing how tolerant this line is to overrun and underruns.")
    allowPartialShipments: bool = Field(description="Allow partial shipments of this line item.")
    unitPrice: decimal.Decimal | None = Field(
        description="The unit price of the line item.",
        default=None
    )
    lineItemTotal: decimal.Decimal = Field(description="The total for the line item.")
    requestedShipDate: date | None = Field(
        description="The date the line item is requested to ship from the FOB point.",
        default=None
    )
    requestedInHandsDate: date | None = Field(description="The date the line item is requested to arrive at the "
                                                          "shipping destination",
                                              default=None)
    referenceSalesQuote: str | None = Field(description="The sales quote number associated with this purchase order "
                                                        "line (if applicable)",
                                            default=None)
    Program: Program | None = Field(
        description="Program pricing information.",
        default=None
    )
    endCustomerSalesOrder: str | None = Field(description="The distributor’s order number provided to the end customer",
                                              default=None)
    productId: str | None = Field(description="The manufacturer’s product id associated with the configuration data",
                                  default=None)
    customerProductId: str | None = Field(description="The distributor’s product id", default=None)
    lineItemGroupingId: int | None = Field(
        description="An identifier that allows configuration data to be spread out "
                    "among multiple purchase order lines. Keep `lineItemGroupingID` "
                    "unique when referencing the same product on the purchase order."
                    "  Any change to the product, location, decoration, or artwork "
                    "should produce a unique `lineItemGroupingID` to the purchase "
                    "order",
        default=None)
    PartArray: PartArray | None = Field(
        description="An array of product part information. This array should be populated with information from the "
                    "supplier’s PromoStandards Product Pricing and Configuration service.",
        default=None
    )
    Configuration: Configuration | None = Field(
        description="An object containing line item configuration data",
        default=None
    )


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
    lastModified: datetime | None = Field(description="The date and time the purchase order was last modified",
                                          default=None)
    totalAmount: decimal.Decimal = Field(description="The total amount of the purchase order")
    paymentTerms: str | None = Field(description="ie. NET15, NET30, etc.", examples=["NET30"], default=None)
    rush: bool = Field(default=False, description="Used to indicate a rush on the purchase order")
    currency: Currency = Field(description="The currency the purchase order is transacted in ISO4217 format."
                                           " ie. USD, CAD, EUR, JPY, GBP, etc.", examples=["USD"])
    DigitalProof: DigitalProof | None = Field(description="An object containing preproduction digital "
                                                          "proof information", default=None)
    OrderContactArray: OrderContactArray | None = Field(description="An array of contact information", default=None)
    ShipmentArray: ShipmentArray = Field(description="Any array of purchase order shipments")
    LineItemArray: LineItemArray = Field(description="An array of purchase order line items")
    termsAndConditions: str = Field(
        description="The terms and conditions for this purchase order. Information that is order specific or "
                    "information dealing with the configuration or shipment of the order should not be entered here.",
        examples=["terms agreed to"])
    salesChannel: str | None = Field(description="The sales channel the purchase order",
                                     examples=["SHOPIFYAPP"], default=None)
    promoCode: str | None = Field(default=None, description="The promotion code",
                                  examples=["SUMMER2023"])
    TaxInformationArray: TaxInformationArray | None = Field(
        description="An array of TaxInformation objects related to calculating taxes.",
        default=None
    )


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
