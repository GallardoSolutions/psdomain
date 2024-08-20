from datetime import date


from .base import ServiceMessageArray, StrEnum, PSBaseModel


class QueryType(StrEnum):
    """
    The type of query to perform for GetInvoices and GetVoidedInvoices
    """
    PO_NUMBER = '1'  # Search for invoices by purchase order number
    INVOICE_NUMBER = '2'  # Search for invoice by invoice number
    DATE = '3'  # Search for invoices with an invoice date specified by the requestedDate
    AVAILABLE_DATE_TIME = '4'  # Search for invoices that were made available by a date time > availableTimeStamp


class VoidedInvoice(PSBaseModel):
    """
    invoiceNumber	The invoice number	64 STRING	TRUE
    voidDate	The date the invoice was voided. This field does not include a time component and it is up to the
                consuming party to determine if the data should be adjusted if the publishing party is on the other
                side of the international date line.	DATE	TRUE
    """
    invoiceNumber: str
    voidDate: date


class VoidedInvoiceArray(PSBaseModel):
    VoidedInvoice: list[VoidedInvoice]


class GetVoidedResponse(PSBaseModel):
    """
    Response from getVoidedInvoices
    """
    VoidedInvoiceArray: VoidedInvoiceArray | None
    ServiceMessageArray: ServiceMessageArray | None


class TaxType(StrEnum):
    """
    All TaxTypes allow in the system: “SALES”, “HST/GST”, “PST”, “VAT”
    """
    SALES = 'SALES'
    HST_GST = 'HST/GST'
    PST = 'PST'
    VAT = 'VAT'


class Tax(PSBaseModel):
    """
    Field	Description	Data Type	Required
    taxType	The type of tax the identifier applies to. Values are enumerated: “SALES”, “HST/GST”, “PST”, “VAT”.	64
            STRING FACIT	TRUE
    taxJurisdiction	The jurisdiction for the tax. For example, NJ, PA or Philadelphia City.	64 SRING	TRUE
    taxAmount	The amount of tax	DOUBLE	TRUE
    """
    taxType: TaxType
    taxJurisdiction: str
    taxAmount: float


class SalesOrderNumber(PSBaseModel):
    """
    Field	Description	Data Type	Required
    salesOrderNumber	The sales order number	64 STRING	TRUE
    """
    salesOrderNumber: str


class SalesOrderNumbersArray(PSBaseModel):
    SalesOrderNumber: list[SalesOrderNumber]


class InvoiceLineItem(PSBaseModel):
    """
    Field	Description	Data Type	Required
    invoiceLineItemNumber	The line item number of the line item	DOUBLE	FALSE
    productId	The productId when the line item applies to a product.	64 STRING	FALSE
    partId	The partId when the line item applies to a product.	64 STRING	FALSE
    chargeId	The chargeId when the line item applies to a charge.	64 STRING	TRUE
    purchaseOrderLineItemNumber	The line item number of the purchase order that the invoice references	64 STRING	FALSE # noqa
    orderedQuantity	The quantity ordered by the referenced purchase order	DOUBLE	FALSE
    invoiceQuantity	The quantity of the line item invoiced.	DOUBLE	TRUE
    backOrderedQuantity	The quantity of the line item backordered.	DOUBLE	FALSE
    quantityUOM	The unit of measure of the orderQuantity, invoicedQuantity, and backOrderedQuantity	2 STRING FACIT	TRUE # noqa
    lineItemDescription	A textual description of the line item	1024 STRING	TRUE
    unitPrice	The price of the unit in the currency of the purchase order	DOUBLE	TRUE
    discountAmount	An amount of discount applied to the item.	DOUBLE	FALSE
    extendedPrice	"The extended price for the line item

    Note: extendedPrice = (unitPrice * invoicedQuantity) - discountAmount"	DOUBLE	TRUE
    distributorProductId	The distributor’s productId for the item when the line item applies to a product.	64 STRING	FALSE  # noqa
    distributorPartId	The distributor’s partId for the item when the line item applies to a product.	64 STRING	FALSE  # noqa
    """
    invoiceLineItemNumber: float | None
    productId: str | None
    partId: str | None
    chargeId: str
    purchaseOrderLineItemNumber: str | None
    orderedQuantity: float | None
    invoiceQuantity: float
    backOrderedQuantity: float | None
    quantityUOM: str
    lineItemDescription: str
    unitPrice: float
    discountAmount: float | None
    extendedPrice: float
    distributorProductId: str | None
    distributorPartId: str | None


class AccountInfo(PSBaseModel):
    """
    accountName	The name of the account that will be invoiced for the purchase order. This also represents the companyName field from the PO.	64 STRING	FALSE  # noqa
    accountNumber	The account number invoiced.	64 STRING	FALSE
    attentionTo	Attention To (first and last name of contact)	64 STRING	FALSE
    address1	Address line 1	35 STRING	FALSE
    address2	Address line 2	35 STRING	FALSE
    address3	Address line 3	35 STRING	FALSE
    city	The city	30 STRING	FALSE
    region	The 2 character US state abbreviation or 2-3 character non-US region.	3 STRING	FALSE
    postalCode	The postal code	10 STRING	FALSE
    country	The country in ISO 3166-2 format	2 STRING	FALSE
    email	The email	128 STRING	FALSE
    phone	The phone number	32 STRING	FALSE
    """
    accountName: str | None
    accountNumber: str | None
    attentionTo: str | None
    address1: str | None
    address2: str | None
    address3: str | None
    city: str | None
    region: str | None
    postalCode: str | None
    country: str | None
    email: str | None
    phone: str | None


class Invoice(PSBaseModel):
    """
    invoiceNumber	The invoice number	64 STRING	TRUE
    invoiceType	The type of invoice; values are enumerated: “INVOICE”, “CREDIT MEMO”. Currency amounts should be positive for type CREDIT MEMO.	64 STRING FACIT	TRUE  # noqa
    invoiceDate	The date the invoice was generated. This field does not include a time component and it is up to the consuming party to determine if the data should be adjusted if the publishing party is on the other side of the international date line.	OBJECT ARRAY	TRUE  # noqa
    purchaseOrderNumber	The purchase order number. Consolidated Purchase Orders are not supported by this version.	64 STRING	FALSE  # noqa
    purchaseOrderVersion	The version of the purchase order number as submitted by the distributor.	64 STRING	FALSE  # noqa
    BillTo	The Bill To Address (AccountInfo Object)	OBJECT	FALSE
    SoldTo	The Sold To Address (AccountInfo Object)	OBJECT	FALSE
    invoiceComments	General comments for the invoice	STRING	FALSE
    paymentTerms	The terms of the invoice	64 STRING	FALSE
    paymentDueDate	The Date the invoice must be paid in full without incurring late charges.	DATE	TRUE
    currency	The currency of the invoice in ISO4217 format	Enumerated STRING	TRUE
    fobId	The fob point of the invoice	64 STRING	FALSE
    salesAmount	The amount of the sale in the currency specified.	DOUBLE	TRUE
    shippingAmount	The amount of the shipping charges in the currency specified.	DOUBLE	TRUE
    handlingAmount	The amount of the handling charges in the currency specified.	DOUBLE	TRUE
    taxAmount	The total amount of taxes in the currency specified.	DOUBLE	TRUE
    invoiceAmount	"The total amount of the invoice in the currency specified.

    Note: invoiceAmount = salesAmount + shippingAmount + handlingAmount + taxAmount"	DOUBLE	TRUE
    advancePaymentAmount	The amount of any advanced payments in the currency specified. If the source system does not support including prepayments on an invoice this value should be set to zero.	DOUBLE	TRUE  # noqa
    invoiceAmountDue	"The total of the invoice amount due after applying any prepayments in the currency specified.

    Note: invoiceAmountDue = invoiceAmount - advancePaymentAmount"	DOUBLE	TRUE
    invoiceDocumentUrl	The url to be able to download the physical invoice document.	1024 STRING	FALSE
    InvoiceLineItemsArray	An array of invoice line item objects	OBJECT ARRAY	TRUE
    SalesOrderNumbersArray	An array of sales order numbers included in the invoice.	OBJECT ARRAY	FALSE
    TaxArray	An array of tax objects. The sum of the taxes within this array should equal the value in the taxAmount field.	OBJECT ARRAY	FALSE  # noqa
    invoicePaymentUrl	The url used to submit payment for the invoice	1024 STRING	FALSE
    """
    invoiceNumber: str
    invoiceType: str
    invoiceDate: date
    purchaseOrderNumber: str | None
    purchaseOrderVersion: str | None
    BillTo: AccountInfo | None
    SoldTo: AccountInfo | None
    invoiceComments: str | None
    paymentTerms: str | None
    paymentDueDate: date
    currency: str
    fobId: str | None
    salesAmount: float
    shippingAmount: float
    handlingAmount: float
    taxAmount: float
    invoiceAmount: float
    advancePaymentAmount: float
    invoiceAmountDue: float
    invoiceDocumentUrl: str | None
    InvoiceLineItemsArray: list[InvoiceLineItem]
    SalesOrderNumbersArray: SalesOrderNumbersArray | None
    TaxArray: list[Tax] | None
    invoicePaymentUrl: str | None


class InvoiceArray(PSBaseModel):
    Invoice: list[Invoice]


class GetInvoiceResponse(PSBaseModel):
    """
    Response object for the getInvoice method.
    """
    InvoiceArray: InvoiceArray | None
    ServiceMessageArray: ServiceMessageArray | None
