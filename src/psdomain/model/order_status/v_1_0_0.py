from datetime import datetime

from ..base import PSBaseModel, ErrorMessage, StrEnum


"""
The service has two endpoints:
    1. getOrderStatusTypes
    2. getOrderStatus
"""


class ResponseTo(PSBaseModel):
    name: str | None
    email_address: str | None
    phone_number: str | None


class ResponseToArray(PSBaseModel):
    ResponseTo: list[ResponseTo]


class OrderStatusDetail(PSBaseModel):
    factoryOrderNumber: str
    statusID: int
    statusName: str  # in the wsdl is required but not in best practice & PromoStandards docs
    responseRequired: bool | None = False  # THe docs say it is required, but we found PCNA sending None
    validTimestamp: datetime
    expectedShipDate: datetime | None
    expectedDeliveryDate: datetime | None
    ResponseToArray: ResponseToArray | None
    additionalExplanation: str | None


class OrderStatusDetailArray(PSBaseModel):
    OrderStatusDetail: list[OrderStatusDetail]


class OrderStatus(PSBaseModel):
    purchaseOrderNumber: str
    OrderStatusDetailArray: OrderStatusDetailArray


class OrderStatusArray(PSBaseModel):
    OrderStatus: list[OrderStatus]


class OrderStatusDetailsResponse(PSBaseModel):
    OrderStatusArray: OrderStatusArray | None
    errorMessage: ErrorMessage | str | None


class QueryType(StrEnum):
    """
    The type of query to perform for GetOrderStatus
    """
    PO_SEARCH = '1'  # Search by Purchase Order Number
    SO_SEARCH = '2'  # Search by Sales Order Number
    LAST_UPDATE_SEARCH = '3'  # Search by Last Update Date with an update time > statusTimeStamp.
    ALL_OPEN_SEARCH = '4'  # Search by All Open Orders that currently have a status not in [“Complete” and “Cancelled”]


class Status(PSBaseModel):
    """
    Possible Statuses according to the reference
    StatusID	Status Name	Description
    10	Order Received	Order has been received.
    11	Order Entry Hold    Vendor has a problem with the data in the purchase order, and it is preventing the order
                            from being entered.
    20	Order Confirmed	Order has been received, entered, and accepted
    30	Pre-Production	Vendor has begun to process the order, but it is not in production
    40	General Hold	Something is preventing the order from being entered
    41	Credit Hold	Vendor is awaiting payment from customer
    42	Proof Hold	Vendor is awaiting response to proof
    43	Art Hold	Vendor is awaiting suitable artwork from customer
    44	Back Order Hold	Order has been backordered; Nothing has shipped yet.
    60	In Production  The production of the order has started
    70	In Storage	Order is complete, but vendor is waiting to ship goods
    75	Partial Shipment	Order has shipped in Part; remaining items in production
    80	Complete	Order has shipped in full—No further updates will be given
    99	Canceled	Order has been canceled—No further updates will be given
    """
    id: int
    name: str


class StatusArray(PSBaseModel):
    Status: list[Status]


class OrderStatusTypesResponse(PSBaseModel):
    """
    Response from getOrderStatusTypes
    """
    StatusArray: StatusArray | None
    errorMessage: str | None
