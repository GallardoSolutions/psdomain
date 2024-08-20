from typing import Optional
from decimal import Decimal
from datetime import date, datetime

from pydantic import HttpUrl, constr, EmailStr, field_validator

from ..base import StrEnum, PSBaseModel, ServiceMessageArray, UOM, \
    String35, String30, String10, String3, String2, String32, String64, String1024, String128

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
    ORDER_ENTRY_HOLD = 'Order Entry Hold'
    GENERAL_HOLD = 'General Hold'
    CREDIT_HOLD = 'Credit Hold'
    PROOF_HOLD = 'Proof Hold'
    ART_HOLD = 'Art Hold'
    BACK_ORDER_HOLD = 'Back Order Hold'
    SHIPPING_HOLD = 'Shipping Hold'
    CUSTOMER_SUPPLIED_ITEM_HOLD = 'Customer Supplied Item Hold'


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
    type: String64
    displayOrder: Optional[int] = None
    required: bool
    length: Optional[int] = None
    pspoFieldName: Optional[String64] = None
    pspoVersion: Optional[String64] = None
    validResponseArray: Optional[ValidResponseToArray] = None


class ParameterArray(PSBaseModel):
    Parameter: list[Parameter]


class Resolution(PSBaseModel):
    resolutionId: String64
    resolutionName: String64
    resolutionDescription: String1024
    ParameterArray: Optional[ParameterArray] = None


class ResolutionArray(PSBaseModel):
    Resolution: list[Resolution]


class Issue(PSBaseModel):
    issueId: String64
    issueStatus: IssueStatus
    issueCategory: String64
    issueName: String64
    urgentResponseRequired: bool
    issueDescription: String1024
    responseRequiredBy: datetime
    issueResolutionURL: HttpUrl
    issueBlockingStatus: String64
    ContactArray: Optional[OrderContactArray] = None
    productId: Optional[String64] = None
    ResolutionArray: Optional[ResolutionArray] = None

    @field_validator('issueResolutionURL')
    def validate_issue_resolution_url(cls, v):
        if not v.startswith('http'):
            raise ValueError('issueResolutionURL must be a valid URL')
        return v

    @field_validator('responseRequiredBy')
    def validate_response_required_by(cls, v):
        if v < datetime.utcnow():
            raise ValueError('responseRequiredBy must be a future date')
        return v

    @field_validator('issueBlockingStatus')
    def validate_issue_blocking_status(cls, v):
        if v not in ('Order Received', 'Order Confirmed', 'Pre-Production', 'In Production', 'In Storage', 'Complete',
                     'Canceled'):
            raise ValueError('issueBlockingStatus must be a valid status')
        return v

    @field_validator('issueCategory')
    def validate_issue_category(cls, v):
        if v not in ('Credit Hold', 'Proof Hold', 'Art Hold', 'Back Order Hold'):
            raise ValueError('issueCategory must be a valid category')
        return v

    @field_validator('issueStatus')
    def validate_issue_status(cls, v):
        if v not in ('Open', 'Closed'):
            raise ValueError('issueStatus must be a valid status')
        return v


class IssueArray(PSBaseModel):
    Issue: list[Issue]


class OrderStatusDetail(PSBaseModel):
    salesOrderNumber: String64
    status: String64
    issueCategory: Optional[String64] = None
    expectedShipDate: Optional[date] = None
    expectedDeliveryDate: Optional[date] = None
    additionalExplanation: Optional[String1024] = None
    qualityProofURL: Optional[HttpUrl] = None
    OrderContactArray: Optional[OrderContactArray] = None
    ProductArray: Optional[ProductArray] = None
    IssueArray: Optional[IssueArray] = None
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


class ServiceMethod(PSBaseModel):
    serviceMethod: String128


class ServiceMethodArray(PSBaseModel):
    ServiceMethod: list[ServiceMethod]


class GetServiceMethodsResponseV200(PSBaseModel):
    ServiceMethodArray: ServiceMethodArray | None
    ServiceMessageArray: ServiceMessageArray | None
