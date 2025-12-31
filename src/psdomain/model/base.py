from __future__ import annotations

import typing
from dataclasses import dataclass
from enum import Enum
import decimal

from pydantic import BaseModel, ConfigDict, constr, model_validator

ZERO = decimal.Decimal(0)


@dataclass
class Event:
    pass


@dataclass
class Command:
    pass


Message = Command | Event


class StrIdentity(str):
    pass


class IntIdentity(int):
    pass


Identity = IntIdentity | StrIdentity

Name = typing.NewType('Name', str)
Email = typing.NewType('Email', str)


class Entity:
    id: Identity


NullableEntity = Entity | None


class StrEnum(str, Enum):

    def __str__(self):
        return self.value


class ServiceCode(StrEnum):
    INV = 'Inventory'
    PPC = 'Price and Configuration'  # Product Price and Configuration
    Product = 'Product Data'
    INVC = 'Invoice'
    ODRSTAT = 'Order Status'
    OSN = 'Order Shipment Notification'
    MED = 'Media Content'
    PO = 'Purchase Order'
    PDC = 'Product Compliance'
    SPCC = 'Supplier Price and Configuration'
    CD = 'Company Data'
    RA = 'Remittance Advice'

    def __str__(self):
        return self.name


class ServiceVersion(StrEnum):
    V_1_0_0 = 'v1.0.0'
    V_1_1_0 = 'v1.1.0'
    V_1_2_1 = 'v1.2.1'
    V_2_0_0 = 'v2.0.0'


class ConfigurationType(StrEnum):
    BLANK = 'Blank'
    DECORATED = 'Decorated'


class PriceType(StrEnum):
    CUSTOMER = 'Customer'
    LIST = 'List'
    NET = 'Net'


class Severity(StrEnum):
    INFO = "Information"
    WARNING = "Warning"
    ERROR = "Error"


class PSBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=False)


class ErrorMessage(PSBaseModel):
    code: int
    description: str

    def __str__(self):
        return f'{self.code} - {self.description}'

    @classmethod
    def not_supported(cls):
        return cls(code=125, description='Not Supported')


def normalize_severity(values):
    try:
        severity = values['severity']
        values['severity'] = severity.capitalize() if severity else 'Error'
    except ValueError:
        raise ValueError(f"Invalid severity value: {values['severity']}")
    return values


class ServiceMessage(PSBaseModel):
    code: int
    description: str
    severity: Severity

    @model_validator(mode='before')
    def normalize_severity(cls, values):
        return normalize_severity(values)

    def __str__(self):
        return f'{self.code} - {self.description} - {self.severity}'

    @classmethod
    def not_supported(cls):
        return cls(code=125, description='Not Supported', severity=Severity.ERROR)


class ServiceMessageArray(PSBaseModel):
    ServiceMessage: list[ServiceMessage]

    def __str__(self):
        return '\n'.join(str(msg) for msg in self.ServiceMessage)

    @classmethod
    def not_supported(cls):
        msg = ServiceMessage.not_supported()
        return cls(ServiceMessage=[msg])


type NullableServiceMessageArray = ServiceMessageArray | None


class Fob(PSBaseModel):
    fobId: str
    fobPostalCode: str | None


class FobArray(PSBaseModel):
    Fob: list[Fob]


ALL_SERVICE_CODES = [
    {
        "Code": "INV",
        "Name": "Inventory"
    },
    {
        "Code": "INVC",
        "Name": "Invoice"
    },
    {
        "Code": "MED",
        "Name": "Media Content"
    },
    {
        "Code": "OSN",
        "Name": "Order Shipment Notification"
    },
    {
        "Code": "ODRSTAT",
        "Name": "Order Status"
    },
    {
        "Code": "PDC",
        "Name": "Product Compliance"
    },
    {
        "Code": "Product",
        "Name": "Product Data"
    },
    {
        "Code": "PPC",
        "Name": "Product Pricing and Configuration"
    },
    {
        "Code": "PO",
        "Name": "Purchase Order"
    },
    {
        "Code": "SPCC",
        "Name": "Service Provider Customer Credentials"
    },
    {
        "Code": "CD",
        "Name": "Company Data"
    },
    {
        "Code": "RA",
        "Name": "Remittance Advice"
    },
]


class WeightUoM(StrEnum):
    ME = 'ME'  # Milligram
    KG = 'KG'  # Kilogram
    OZ = 'OZ'  # Ounce
    LB = 'LB'  # Pound


class DimensionUoM(StrEnum):
    MM = 'MM'  # Millimeter
    CM = 'CM'  # Centimeter
    MR = 'MR'  # Meter
    IN = 'IN'  # Inch
    FT = 'FT'  # Feet
    YD = 'YD'  # Yards


class CountryIso2(StrEnum):
    AX = "AX"
    AL = "AL"
    DZ = "DZ"
    AS = "AS"
    AD = "AD"
    AO = "AO"
    AI = "AI"
    AQ = "AQ"
    AG = "AG"
    AR = "AR"
    AM = "AM"
    AW = "AW"
    AU = "AU"
    AT = "AT"
    AZ = "AZ"
    BS = "BS"
    BH = "BH"
    BD = "BD"
    BB = "BB"
    BY = "BY"
    BE = "BE"
    BZ = "BZ"
    BJ = "BJ"
    BM = "BM"
    BT = "BT"
    BO = "BO"
    BA = "BA"
    BW = "BW"
    BV = "BV"
    BR = "BR"
    IO = "IO"
    BN = "BN"
    BG = "BG"
    BF = "BF"
    BI = "BI"
    KH = "KH"
    CM = "CM"
    CA = "CA"
    CV = "CV"
    KY = "KY"
    CF = "CF"
    TD = "TD"
    CL = "CL"
    CN = "CN"
    CX = "CX"
    CC = "CC"
    CO = "CO"
    KM = "KM"
    CG = "CG"
    CD = "CD"
    CK = "CK"
    CR = "CR"
    CI = "CI"
    HR = "HR"
    CU = "CU"
    CY = "CY"
    CZ = "CZ"
    DK = "DK"
    DJ = "DJ"
    DM = "DM"
    DO = "DO"
    EC = "EC"
    EG = "EG"
    SV = "SV"
    GQ = "GQ"
    ER = "ER"
    EE = "EE"
    ET = "ET"
    FK = "FK"
    FO = "FO"
    FJ = "FJ"
    FI = "FI"
    FR = "FR"
    GF = "GF"
    PF = "PF"
    TF = "TF"
    GA = "GA"
    GM = "GM"
    GE = "GE"
    DE = "DE"
    GH = "GH"
    GI = "GI"
    GR = "GR"
    GL = "GL"
    GD = "GD"
    GP = "GP"
    GU = "GU"
    GT = "GT"
    GG = "GG"
    GN = "GN"
    GW = "GW"
    GY = "GY"
    HT = "HT"
    HM = "HM"
    VA = "VA"
    HN = "HN"
    HK = "HK"
    HU = "HU"
    IS = "IS"
    IN = "IN"
    ID = "ID"
    IR = "IR"
    IQ = "IQ"
    IE = "IE"
    IM = "IM"
    IL = "IL"
    IT = "IT"
    JM = "JM"
    JP = "JP"
    JE = "JE"
    JO = "JO"
    KZ = "KZ"
    KE = "KE"
    KI = "KI"
    KP = "KP"
    KR = "KR"
    KW = "KW"
    KG = "KG"
    LA = "LA"
    LV = "LV"
    LB = "LB"
    LS = "LS"
    LR = "LR"
    LY = "LY"
    LI = "LI"
    LT = "LT"
    LU = "LU"
    MO = "MO"
    MK = "MK"
    MG = "MG"
    MW = "MW"
    MY = "MY"
    MV = "MV"
    ML = "ML"
    MT = "MT"
    MH = "MH"
    MQ = "MQ"
    MR = "MR"
    MU = "MU"
    YT = "YT"
    MX = "MX"
    FM = "FM"
    MD = "MD"
    MC = "MC"
    MN = "MN"
    MS = "MS"
    MA = "MA"
    MZ = "MZ"
    MM = "MM"
    NA = "NA"
    NR = "NR"
    NP = "NP"
    NL = "NL"
    AN = "AN"
    NC = "NC"
    NZ = "NZ"
    NI = "NI"
    NE = "NE"
    NG = "NG"
    NU = "NU"
    NF = "NF"
    MP = "MP"
    NO = "NO"
    OM = "OM"
    PK = "PK"
    PW = "PW"
    PS = "PS"
    PA = "PA"
    PG = "PG"
    PY = "PY"
    PE = "PE"
    PH = "PH"
    PN = "PN"
    PL = "PL"
    PT = "PT"
    PR = "PR"
    QA = "QA"
    RE = "RE"
    RO = "RO"
    RU = "RU"
    RW = "RW"
    SH = "SH"
    KN = "KN"
    LC = "LC"
    PM = "PM"
    VC = "VC"
    WS = "WS"
    SM = "SM"
    ST = "ST"
    SA = "SA"
    SN = "SN"
    CS = "CS"
    SC = "SC"
    SL = "SL"
    SG = "SG"
    SK = "SK"
    SI = "SI"
    SB = "SB"
    SO = "SO"
    ZA = "ZA"
    GS = "GS"
    ES = "ES"
    LK = "LK"
    SD = "SD"
    SR = "SR"
    SJ = "SJ"
    SZ = "SZ"
    SE = "SE"
    CH = "CH"
    SY = "SY"
    TW = "TW"
    TJ = "TJ"
    TZ = "TZ"
    TH = "TH"
    TL = "TL"
    TG = "TG"
    TK = "TK"
    TO = "TO"
    TT = "TT"
    TN = "TN"
    TR = "TR"
    TM = "TM"
    TC = "TC"
    TV = "TV"
    UG = "UG"
    UA = "UA"
    AE = "AE"
    GB = "GB"
    US = "US"
    UM = "UM"
    UY = "UY"
    UZ = "UZ"
    VU = "VU"
    VE = "VE"
    VN = "VN"
    VG = "VG"
    VI = "VI"
    WF = "WF"
    EH = "EH"
    YE = "YE"
    ZM = "ZM"
    ZW = "ZW"


class UOM(StrEnum):
    """
    Unit of Measurement
    BX - Box
    CA - Case
    DZ - Dozen
    EA - Each
    KT - Kit
    PR - Pair
    PK - Package
    RL - Roll
    ST - Set
    SL - Sleeve
    TH – Thousand
    """
    BX = 'BX'
    CA = 'CA'
    DZ = 'DZ'
    EA = 'EA'
    KT = 'KT'
    PR = 'PR'
    PK = 'PK'
    RL = 'RL'
    ST = 'ST'
    SL = 'SL'
    TH = 'TH'


class Environment(StrEnum):
    PROD = 'PROD'
    STAGING = 'STAGING'


String64 = constr(max_length=64)
String1024 = constr(max_length=1024)
String35 = constr(max_length=35)
String30 = constr(max_length=30)
String3 = constr(max_length=3)
String10 = constr(max_length=10)
String2 = constr(max_length=2)
String128 = constr(max_length=128)
String32 = constr(max_length=32)
String256 = constr(max_length=256)


class QuantityUoM(StrEnum):
    """
    BX - Box
    CA - Case
    DZ - Dozen
    EA - Each
    KT - Kit
    PR - Pair
    PK - Package
    RL - Roll
    ST - Set
    SL - Sleeve
    TH - Thousand
    """
    BX = "BX"
    CA = "CA"
    DZ = "DZ"
    EA = "EA"
    KT = "KT"
    PR = "PR"
    PK = "PK"
    RL = "RL"
    ST = "ST"
    SL = "SL"
    TH = "TH"


class Quantity(PSBaseModel):
    value: decimal.Decimal
    uom: QuantityUoM


class Currency(StrEnum):
    """
    The currency the purchase order is transacted in ISO4217 format. ie. USD, CAD, etc.
    """
    AED = "AED"  # United Arab Emirates Dirham
    AFN = "AFN"  # Afghan Afghani
    ALL = "ALL"  # Albanian Lek
    AMD = "AMD"  # Armenian Dram
    ANG = "ANG"  # Netherlands Antillean Guilder
    AOA = "AOA"  # Angolan Kwanza
    ARS = "ARS"  # Argentine Peso
    AUD = "AUD"  # Australian Dollar
    AWG = "AWG"  # Aruban Florin
    AZN = "AZN"  # Azerbaijani Manat
    BAM = "BAM"  # Bosnia and Herzegovina Convertible Mark
    BBD = "BBD"  # Barbadian Dollar
    BDT = "BDT"  # Bangladeshi Taka
    BGN = "BGN"  # Bulgarian Lev
    BHD = "BHD"  # Bahraini Dinar
    BIF = "BIF"  # Burundian Franc
    BMD = "BMD"  # Bermudian Dollar
    BND = "BND"  # Brunei Dollar
    BOB = "BOB"  # Bolivian Boliviano
    BOV = "BOV"  # Bolivian Mvdol (funds code)
    BRL = "BRL"  # Brazilian Real
    BSD = "BSD"  # Bahamian Dollar
    BTN = "BTN"  # Bhutanese Ngultrum
    BWP = "BWP"  # Botswanan Pula
    BYN = "BYN"  # Belarusian Ruble
    BYR = "BYR"  # Belarusian Ruble (1992–2016)
    BZD = "BZD"  # Belize Dollar
    CAD = "CAD"  # Canadian Dollar
    CDF = "CDF"  # Congolese Franc
    CHE = "CHE"  # WIR Euro (complementary currency)
    CHF = "CHF"  # Swiss Franc
    CHW = "CHW"  # WIR Franc (complementary currency)
    CLP = "CLP"  # Chilean Peso
    CNY = "CNY"  # Chinese Yuan Renminbi
    COP = "COP"  # Colombian Peso
    COU = "COU"  # Unidad de Valor Real (UVR) (Colombia)
    CRC = "CRC"  # Costa Rican Colon
    CUP = "CUP"  # Cuban Peso
    CVE = "CVE"  # Cape Verdean Escudo
    CZK = "CZK"  # Czech Koruna
    DJF = "DJF"  # Djiboutian Franc
    DKK = "DKK"  # Danish Krone
    DOP = "DOP"  # Dominican Peso
    DZD = "DZD"  # Algerian Dinar
    EGP = "EGP"  # Egyptian Pound
    ERN = "ERN"  # Eritrean Nakfa
    ETB = "ETB"  # Ethiopian Birr
    EUR = "EUR"  # Euro
    FJD = "FJD"  # Fijian Dollar
    FKP = "FKP"  # Falkland Islands Pound
    GBP = "GBP"  # British Pound Sterling
    GEL = "GEL"  # Georgian Lari
    GHS = "GHS"  # Ghanaian Cedi
    GIP = "GIP"  # Gibraltar Pound
    GMD = "GMD"  # Gambian Dalasi
    GNF = "GNF"  # Guinean Franc
    GTQ = "GTQ"  # Guatemalan Quetzal
    GYD = "GYD"  # Guyanese Dollar
    HKD = "HKD"  # Hong Kong Dollar
    HNL = "HNL"  # Honduran Lempira
    HRK = "HRK"  # Croatian Kuna
    HTG = "HTG"  # Haitian Gourde
    HUF = "HUF"  # Hungarian Forint
    IDR = "IDR"  # Indonesian Rupiah
    ILS = "ILS"  # Israeli New Shekel
    INR = "INR"  # Indian Rupee
    IQD = "IQD"  # Iraqi Dinar
    IRR = "IRR"  # Iranian Rial
    ISK = "ISK"  # Icelandic Krona
    JMD = "JMD"  # Jamaican Dollar
    JOD = "JOD"  # Jordanian Dinar
    JPY = "JPY"  # Japanese Yen
    KES = "KES"  # Kenyan Shilling
    KGS = "KGS"  # Kyrgyzstani Som
    KHR = "KHR"  # Cambodian Riel
    KMF = "KMF"  # Comorian Franc
    KPW = "KPW"  # North Korean Won
    KRW = "KRW"  # South Korean Won
    KWD = "KWD"  # Kuwaiti Dinar
    KYD = "KYD"  # Cayman Islands Dollar
    KZT = "KZT"  # Kazakhstani Tenge
    LAK = "LAK"  # Laotian Kip
    LBP = "LBP"  # Lebanese Pound
    LKR = "LKR"  # Sri Lankan Rupee
    LRD = "LRD"  # Liberian Dollar
    LSL = "LSL"  # Lesotho Loti
    LTL = "LTL"  # Lithuanian Litas
    LYD = "LYD"  # Libyan Dinar
    MAD = "MAD"  # Moroccan Dirham
    MDL = "MDL"  # Moldovan Leu
    MGA = "MGA"  # Malagasy Ariary
    MKD = "MKD"  # Macedonian Denar
    MMK = "MMK"  # Burmese Kyat
    MNT = "MNT"  # Mongolian Tugrik
    MOP = "MOP"  # Macanese Pataca
    MRO = "MRO"  # Mauritanian Ouguiya
    MUR = "MUR"  # Mauritian Rupee
    MVR = "MVR"  # Maldivian Rufiyaa
    MWK = "MWK"  # Malawian Kwacha
    MXN = "MXN"  # Mexican Peso
    MYR = "MYR"  # Malaysian Ringgit
    MZN = "MZN"  # Mozambican Metical
    NAD = "NAD"  # Namibian Dollar
    NGN = "NGN"  # Nigerian Naira
    NIO = "NIO"  # Nicaraguan Cordoba
    NOK = "NOK"  # Norwegian Krone
    NPR = "NPR"  # Nepalese Rupee
    NZD = "NZD"  # New Zealand Dollar
    OMR = "OMR"  # Omani Rial
    PAB = "PAB"  # Panamanian Balboa
    PEN = "PEN"  # Peruvian Sol
    PGK = "PGK"  # Papua New Guinean Kina
    PHP = "PHP"  # Philippine Peso
    PKR = "PKR"  # Pakistani Rupee
    PLN = "PLN"  # Polish Zloty
    PYG = "PYG"  # Paraguayan Guarani
    QAR = "QAR"  # Qatari Riyal
    RON = "RON"  # Romanian Leu
    RSD = "RSD"  # Serbian Dinar
    RUB = "RUB"  # Russian Ruble
    RWF = "RWF"  # Rwandan Franc
    SAR = "SAR"  # Saudi Arabian Riyal
    SBD = "SBD"  # Solomon Islands Dollar
    SCR = "SCR"  # Seychellois Rupee
    SDG = "SDG"  # Sudanese Pound
    SEK = "SEK"  # Swedish Krona
    SGD = "SGD"  # Singapore Dollar
    SHP = "SHP"  # Saint Helena Pound
    SLL = "SLL"  # Sierra Leonean Leone
    SOS = "SOS"  # Somali Shilling
    SRD = "SRD"  # Surinamese Dollar
    SSP = "SSP"  # South Sudanese Pound
    SYP = "SYP"  # Syrian Pound
    SZL = "SZL"  # Swazi Lilangeni
    THB = "THB"  # Thai Baht
    TJS = "TJS"  # Tajikistani Somoni
    TMT = "TMT"  # Turkmenistani Manat
    TND = "TND"  # Tunisian Dinar
    TOP = "TOP"  # Tongan Paʻanga
    TRY = "TRY"  # Turkish Lira
    TTD = "TTD"  # Trinidad and Tobago Dollar
    TWD = "TWD"  # New Taiwan Dollar
    TZS = "TZS"  # Tanzanian Shilling
    UAH = "UAH"  # Ukrainian Hryvnia
    UGX = "UGX"  # Ugandan Shilling
    USD = "USD"  # United States Dollar
    UZS = "UZS"  # Uzbekistani Som
    VND = "VND"  # Vietnamese Dong
    VUV = "VUV"  # Vanuatu Vatu
    WST = "WST"  # Samoan Tala
    YER = "YER"  # Yemeni Rial
    ZAR = "ZAR"  # South African Rand
    ZMK = "ZMK"  # Zambian Kwacha (1968–2012)
    ZMW = "ZMW"  # Zambian Kwacha


class ErrorMessageResponse(PSBaseModel):
    ErrorMessage: ErrorMessage | None

    @property
    def is_ok(self):
        return self.ErrorMessage is None

    @property
    def errors(self):
        return str(self.ErrorMessage) if self.ErrorMessage else None

    @classmethod
    def not_supported(cls):
        field_name = [k for k in cls.model_fields.keys() if k != 'ErrorMessage'][0]
        return cls(**{field_name: None, 'ErrorMessage': ErrorMessage.not_supported()})


class ServiceMessageResponse(PSBaseModel):
    ServiceMessageArray: ServiceMessageArray | None

    @property
    def is_ok(self):
        return self.ServiceMessageArray is None

    @property
    def errors(self):
        return str(self.ServiceMessageArray) if self.ServiceMessageArray else None

    @classmethod
    def not_supported(cls):
        field_name = [k for k in cls.model_fields.keys() if k != 'ServiceMessageArray'][0]
        return cls(**{field_name: None, 'ServiceMessageArray': ServiceMessageArray.not_supported()})
