from typing import Optional
from decimal import Decimal
from datetime import date, datetime

from pydantic import constr, EmailStr, field_validator

from ..base import StrEnum, PSBaseModel, ServiceMessageArray, NullableServiceMessageArray, UOM, \
    String35, String30, String10, String3, String2, String32, String64, String1024

"""
The service has three endpoints:
- getOrderStatus
- getIssues
- getServiceMethods
"""


class ContactType(StrEnum):
    """
    The type of contact
    Art, Bill, Expeditor, Order, Sales, Sold
    """
    ART = 'Art'
    BILL = 'Bill'
    EXPEDITOR = 'Expeditor'
    ORDER = 'Order'
    SALES = 'Sales'
    SOLD = 'Sold'


class IssueStatus(StrEnum):
    """
    The status of the issue
    Pending, Open, Closed
    """
    PENDING = 'Pending'
    OPEN = 'Open'
    CLOSED = 'Closed'


class IssueCategory(StrEnum):
    # issueCategoryType in the Order Status 2.0.0 WSDL
    ORDER_ENTRY_HOLD = 'orderEntryHold'
    GENERAL_HOLD = 'generalHold'
    CREDIT_HOLD = 'creditHold'
    PROOF_HOLD = 'proofHold'
    ART_HOLD = 'artHold'
    BACK_ORDER_HOLD = 'backOrderHold'
    SHIPPING_HOLD = 'shippingHold'
    CUSTOMER_SUPPLIED_ITEM_HOLD = 'customerSuppliedItemHold'


class Status(StrEnum):
    RECEIVED = 'received'
    CONFIRMED = 'confirmed'
    PREPRODUCTION = 'preproduction'
    IN_PRODUCTION = 'inProduction'
    IN_STORAGE = 'inStorage'
    PARTIALLY_SHIPPED = 'partiallyShipped'
    SHIPPED = 'shipped'
    COMPLETE = 'complete'
    CANCELED = 'canceled'


class ContactDetails(PSBaseModel):
    attentionTo: Optional[String35] = None
    companyName: Optional[String35] = None
    address1: Optional[String35] = None
    address2: Optional[String35] = None
    address3: Optional[String35] = None
    city: Optional[String30] = None
    region: Optional[String3] = None
    postalCode: Optional[String10] = None
    country: Optional[String2] = None
    email: Optional[EmailStr] = None
    phone: Optional[String32] = None
    comments: Optional[str] = None


class Contact(PSBaseModel):
    accountName: Optional[String64] = None
    accountNumber: Optional[String64] = None
    contactType: ContactType
    contactDetails: ContactDetails


class OrderContactArray(PSBaseModel):
    Contact: list[Contact]


class Quantity(PSBaseModel):
    value: Decimal
    uom: UOM

    @field_validator('value')
    def validate_value(cls, v):
        if v < 0:
            raise ValueError('Quantity must be a non-negative integer')
        return v


class Product(PSBaseModel):
    productId: String64
    partId: Optional[String64] = None
    salesOrderLineNumber: String64
    purchaseOrderLineNumber: Optional[String64] = None
    QuantityOrdered: Quantity
    QuantityShipped: Optional[Quantity] = None
    issueCategory: Optional[IssueCategory] = None
    status: Status


class ProductArray(PSBaseModel):
    Product: list[Product]


class ValidResponseTo(PSBaseModel):
    value: str


class ValidResponseToArray(PSBaseModel):
    ValidResponseTo: list[ValidResponseTo]


class Parameter(PSBaseModel):
    parameterId: String64
    name: String64
    type: Optional[String64] = None
    displayOrder: Optional[int] = None
    required: bool
    length: Optional[int] = None
    pspoFieldName: Optional[String64] = None
    pspoVersion: Optional[String64] = None
    validResponseArray: Optional[ValidResponseToArray] = None


class ParameterArray(PSBaseModel):
    Parameter: list[Parameter]


# Python 3.14 evaluates annotations lazily in the class namespace, where a field's default (None)
# shadows a class of the same name; fields named after their type annotate through these aliases.
_ParameterArray = ParameterArray


class Resolution(PSBaseModel):
    resolutionId: String64
    resolutionName: String64
    resolutionDescription: String1024
    ParameterArray: Optional[_ParameterArray] = None


class ResolutionArray(PSBaseModel):
    Resolution: list[Resolution]


_ResolutionArray = ResolutionArray


class Issue(PSBaseModel):
    """Issue as the Order Status 2.0.0 WSDL defines it: only issueStatus, issueCategory and urgentResponseRequired
    are required. issueResolutionURL is xsd:string, not a URL type."""
    issueId: Optional[String64] = None
    issueStatus: IssueStatus
    issueCategory: IssueCategory
    issueName: Optional[String64] = None
    urgentResponseRequired: bool
    issueDescription: Optional[String1024] = None
    responseRequiredBy: Optional[datetime] = None
    issueResolutionURL: Optional[String1024] = None
    ResolutionArray: Optional[_ResolutionArray] = None
    issueBlockingStatus: Optional[Status] = None
    ContactArray: Optional[OrderContactArray] = None
    productId: Optional[String64] = None
    partId: Optional[String64] = None


class IssueArray(PSBaseModel):
    Issue: list[Issue]


_OrderContactArray, _ProductArray, _IssueArray = OrderContactArray, ProductArray, IssueArray


class OrderStatusDetail(PSBaseModel):
    salesOrderNumber: String64
    status: String64
    issueCategory: Optional[String64] = None
    expectedShipDate: Optional[date] = None
    expectedDeliveryDate: Optional[date] = None
    additionalExplanation: Optional[String1024] = None
    qualityProofURL: Optional[String1024] = None  # xsd:string in the WSDL, not a URL type
    OrderContactArray: Optional[_OrderContactArray] = None
    ProductArray: Optional[_ProductArray] = None
    IssueArray: Optional[_IssueArray] = None
    validTimestamp: datetime


class OrderStatusDetailArray(PSBaseModel):
    OrderStatusDetail: list[OrderStatusDetail]


class OrderStatus(PSBaseModel):
    purchaseOrderNumber: constr(min_length=1, max_length=64)
    OrderStatusDetailArray: OrderStatusDetailArray
    auditURL: constr(min_length=1, max_length=1024) | None = None


class OrderStatusArray(PSBaseModel):
    OrderStatus: list[OrderStatus]


class GetOrderStatusResponseV200(PSBaseModel):
    OrderStatusArray: OrderStatusArray | None
    ServiceMessageArray: ServiceMessageArray | None


class GetIssueResponseV200(PSBaseModel):
    IssueArray: IssueArray | None
    ServiceMessageArray: ServiceMessageArray | None


class ServiceMethodArray(PSBaseModel):
    # WSDL: a flat list of serviceMethod strings (1-128 chars), with no wrapper element per method
    serviceMethod: list[constr(min_length=1, max_length=128)]


_ServiceMethodArray = ServiceMethodArray


class GetServiceMethodsResponseV200(PSBaseModel):
    ServiceMethodArray: Optional[_ServiceMethodArray] = None
    ServiceMessageArray: NullableServiceMessageArray = None
