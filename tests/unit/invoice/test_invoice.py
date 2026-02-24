# flake8: noqa F811
from .fixtures import invoice_response_ok_obj  # noqa


def test_import_invoice_models():
    """Verifies that importing invoice models doesn't crash (the original bug)."""
    from psdomain.model.invoice import (
        GetInvoiceResponse, Invoice, InvoiceArray,
        BillTo, SoldTo, TaxArray, SalesOrderNumbersArray,
        InvoiceLineItemsArray,
    )
    assert GetInvoiceResponse is not None


def test_invoice_response_ok(invoice_response_ok_obj):
    """Validates parsing succeeds and InvoiceArray is populated."""
    resp = invoice_response_ok_obj
    assert resp.is_ok
    assert resp.InvoiceArray is not None
    assert len(resp.InvoiceArray.Invoice) == 2


def test_bill_to_wrapper(invoice_response_ok_obj):
    """Access invoice.BillTo.AccountInfo.accountName."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    assert invoice.BillTo is not None
    assert invoice.BillTo.AccountInfo.accountName == "Acme Corp"


def test_sold_to_wrapper(invoice_response_ok_obj):
    """Access invoice.SoldTo.AccountInfo.city."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    assert invoice.SoldTo is not None
    assert invoice.SoldTo.AccountInfo.city == "Los Angeles"


def test_address_casing_normalization(invoice_response_ok_obj):
    """PascalCase Address1/Address2/Address3 mapped to camelCase fields."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    bill_to_info = invoice.BillTo.AccountInfo
    assert bill_to_info.address1 == "123 Main St"
    assert bill_to_info.address2 == "Suite 400"
    assert bill_to_info.address3 == "Building B"


def test_invoice_line_items_wrapper(invoice_response_ok_obj):
    """Access invoice.InvoiceLineItemsArray.InvoiceLineItem[0].productId."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    items = invoice.InvoiceLineItemsArray.InvoiceLineItem
    assert len(items) == 1
    assert items[0].productId == "PROD-100"


def test_tax_array_wrapper(invoice_response_ok_obj):
    """Access invoice.TaxArray.tax[0].taxAmount."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    assert invoice.TaxArray is not None
    taxes = invoice.TaxArray.tax
    assert len(taxes) == 2
    assert taxes[0].taxAmount == 40.00


def test_fob_field_name(invoice_response_ok_obj):
    """Verify invoice.fob works (not fobId)."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    assert invoice.fob == "Origin"


def test_optional_fields_none(invoice_response_ok_obj):
    """Invoice with missing optional fields parses correctly."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[1]
    assert invoice.BillTo is None
    assert invoice.SoldTo is None
    assert invoice.TaxArray is None
    assert invoice.SalesOrderNumbersArray is None
    assert invoice.fob is None
    assert invoice.invoiceComments is None
    assert invoice.invoicePaymentUrl is None


def test_sales_order_numbers_wrapper(invoice_response_ok_obj):
    """Access invoice.SalesOrderNumbersArray.SalesOrderNumber[0].salesOrderNumber."""
    invoice = invoice_response_ok_obj.InvoiceArray.Invoice[0]
    assert invoice.SalesOrderNumbersArray is not None
    orders = invoice.SalesOrderNumbersArray.SalesOrderNumber
    assert len(orders) == 2
    assert orders[0].salesOrderNumber == "SO-9001"
    assert orders[1].salesOrderNumber == "SO-9002"
