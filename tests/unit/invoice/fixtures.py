import pytest

from psdomain.model.invoice import GetInvoiceResponse
from .responses.invoices import invoice_response_ok


@pytest.fixture
def invoice_response_ok_obj() -> GetInvoiceResponse:
    yield GetInvoiceResponse.model_validate(invoice_response_ok)
