from ..base import StrEnum


class QueryType(StrEnum):
    """
    query to perform for getOrderShipmentNotification
    """
    PO_SEARCH = '1'  # Search by Purchase Order Number
    SO_SEARCH = '2'  # Search by Sales Order Number
    SHIP_DATE_SEARCH = '3'  # Search by Ship Date with a shipment date > shipmentDateTimeStamp.


class DimUOM(StrEnum):
    """
    Dimensions Unit of Measure
    """
    INCHES = 'Inches'
    FEET = 'Feet'
    MM = 'mm'
    CM = 'cm'
    METERS = 'Meters'


class WeightUOM(StrEnum):
    """
    Weight Unit of Measure
    """
    OUNCES = 'Ounces'
    POUNDS = 'Pounds'
    GRAMS = 'Grams'
    KG = 'KG'


class ShipmentDestinationType(StrEnum):
    """
    Shipment Destination Types allowed
    """
    COMMERCIAL = 'Commercial'
    RESIDENTIAL = 'Residential'
    NONE = 'None'


class PreProductionProofType(StrEnum):
    """
    Pre-Production Proof Type
    """
    YES = 'Yes'
    NO = 'No'
    UNKNOWN = 'Unknown'


TRACKING_URLS = {
    "USPS": "https://tools.usps.com/go/TrackConfirmAction?tLabels={}",
    "UPS": "https://www.ups.com/track?tracknum={}",
    "FEDEX": "https://www.fedex.com/fedextrack/?trknbr={}",
    "DHL": "https://www.dhl.com/en/express/tracking.html?AWB={}",
}
