import pytest
from pydantic import ValidationError

from psdomain.model.order_status.v_2_0_0 import GetServiceMethodsResponseV200, Issue, OrderStatusDetail, Product


PRODUCT = {
    "productId": "FSB105", "partId": "FSB105-ORANGE", "salesOrderLineNumber": "1", "purchaseOrderLineNumber": "1",
    "QuantityOrdered": {"value": "100", "uom": "EA"}, "QuantityShipped": {"value": "0", "uom": "EA"},
    "issueCategory": None, "status": "confirmed",
}


def _detail(**extra):
    return {
        "salesOrderNumber": "SO-1",
        "status": "confirmed",
        "validTimestamp": "2026-11-18T00:00:00+00:00",
        **extra,
    }


def test_order_status_detail_accepts_a_product_array():
    """Lincoln Line (2026-11-22): a filled ProductArray was rejected with "Input should be None" on Python 3.14."""
    detail = OrderStatusDetail.model_validate(_detail(ProductArray={"Product": [{
        "productId": "FSB105",
        "partId": "FSB105-ORANGE",
        "salesOrderLineNumber": "1",
        "purchaseOrderLineNumber": "1",
        "QuantityOrdered": {"value": "100", "uom": "EA"},
        "QuantityShipped": {"value": "0", "uom": "EA"},
        "issueCategory": None,
        "status": "confirmed",
    }]}))

    assert detail.ProductArray.Product[0].partId == "FSB105-ORANGE"


def test_order_status_detail_accepts_an_order_contact_array():
    detail = OrderStatusDetail.model_validate(_detail(OrderContactArray={"Contact": []}))

    assert detail.OrderContactArray is not None


# Values from the Order Status 2.0.0 WSDL (psrestful-api src/ps/entrypoints/fast_api/templates/odrstat/200.xml).
ISSUE = {
    "issueId": "I-1", "issueStatus": "Open", "issueCategory": "proofHold", "issueName": "Proof",
    "urgentResponseRequired": False, "issueDescription": "Approve the proof",
    "responseRequiredBy": "2030-01-01T00:00:00+00:00", "issueResolutionURL": "https://example.com/issue/1",
    "issueBlockingStatus": "inProduction",
}


def test_issue_accepts_resolutions_with_parameters():
    issue = Issue.model_validate({**ISSUE, "ResolutionArray": {"Resolution": [{
        "resolutionId": "R-1", "resolutionName": "Approve", "resolutionDescription": "Approve as is",
        "ParameterArray": {"Parameter": [{"parameterId": "P-1", "name": "comment", "required": False}]},
    }]}})

    resolution = issue.ResolutionArray.Resolution[0]
    assert resolution.resolutionId == "R-1"
    assert resolution.ParameterArray.Parameter[0].type is None  # minOccurs=0 in the WSDL


def test_issue_needs_only_the_wsdl_required_elements():
    """issueStatus, issueCategory and urgentResponseRequired are the only required Issue elements."""
    issue = Issue.model_validate({"issueStatus": "Pending", "issueCategory": "creditHold",
                                  "urgentResponseRequired": True})

    assert (issue.issueId, issue.responseRequiredBy, issue.issueResolutionURL, issue.issueBlockingStatus) == \
        (None, None, None, None)


@pytest.mark.parametrize("category", ["orderEntryHold", "generalHold", "creditHold", "proofHold", "artHold",
                                      "backOrderHold", "shippingHold", "customerSuppliedItemHold"])
def test_issue_and_product_accept_every_wsdl_issue_category(category):
    assert Issue.model_validate({**ISSUE, "issueCategory": category}).issueCategory == category
    assert Product.model_validate({**PRODUCT, "issueCategory": category}).issueCategory == category


@pytest.mark.parametrize("status", ["Pending", "Open", "Closed"])
def test_issue_accepts_every_wsdl_issue_status(status):
    assert Issue.model_validate({**ISSUE, "issueStatus": status}).issueStatus == status


@pytest.mark.parametrize("blocking", ["received", "confirmed", "preproduction", "inProduction", "inStorage",
                                      "partiallyShipped", "shipped", "complete", "canceled"])
def test_issue_accepts_every_wsdl_blocking_status(blocking):
    assert Issue.model_validate({**ISSUE, "issueBlockingStatus": blocking}).issueBlockingStatus == blocking


@pytest.mark.parametrize("when", ["2030-01-01T00:00:00+00:00", "2030-01-01T00:00:00", "2020-01-01T00:00:00-05:00"])
def test_issue_accepts_any_response_required_by(when):
    """A deadline with or without an offset, and one already past, is the supplier's data, not an invalid answer."""
    issue = Issue.model_validate({**ISSUE, "responseRequiredBy": when})

    assert issue.responseRequiredBy.year in (2020, 2030)


def test_issue_resolution_url_is_a_plain_string():
    """The WSDL types issueResolutionURL as xsd:string (1-1024), not as a URL."""
    issue = Issue.model_validate({**ISSUE, "issueResolutionURL": "portal: order 123, issue 1"})

    assert issue.issueResolutionURL == "portal: order 123, issue 1"


def test_issue_keeps_the_part_id():
    assert Issue.model_validate({**ISSUE, "productId": "FSB105", "partId": "FSB105-ORANGE"}).partId == "FSB105-ORANGE"


def test_issue_rejects_a_category_outside_the_wsdl():
    with pytest.raises(ValidationError):
        Issue.model_validate({**ISSUE, "issueCategory": "Proof Hold"})


def test_order_status_detail_accepts_an_issue_array():
    detail = OrderStatusDetail.model_validate(_detail(IssueArray={"Issue": [ISSUE]}))

    assert detail.IssueArray.Issue[0].issueId == "I-1"


def test_quality_proof_url_is_a_plain_string():
    """The WSDL types qualityProofURL as xsd:string (1-1024): keep what the supplier sent, as sent."""
    for value in ("https://proofs.example.com/SO-1", "proof sent by email"):
        assert OrderStatusDetail.model_validate(_detail(qualityProofURL=value)).qualityProofURL == value


def test_get_service_methods_reads_the_wsdl_flat_list():
    """SanMar (2026-11-18): ServiceMethodArray holds serviceMethod strings, as the WSDL says; it was rejected."""
    response = GetServiceMethodsResponseV200.model_validate({
        "ServiceMethodArray": {"serviceMethod": ["getOrderStatus", "getIssue", "getServiceMethods"]},
        "ServiceMessageArray": None,
    })

    assert response.ServiceMethodArray.serviceMethod == ["getOrderStatus", "getIssue", "getServiceMethods"]


def test_get_service_methods_allows_both_arrays_to_be_missing():
    response = GetServiceMethodsResponseV200.model_validate({})

    assert response.ServiceMethodArray is None
    assert response.ServiceMessageArray is None


def test_get_service_methods_rejects_the_old_nested_shape():
    with pytest.raises(ValidationError):
        GetServiceMethodsResponseV200.model_validate({
            "ServiceMethodArray": {"ServiceMethod": [{"serviceMethod": "getOrderStatus"}]},
        })


def test_get_service_methods_rejects_an_empty_method_name():
    with pytest.raises(ValidationError):
        GetServiceMethodsResponseV200.model_validate({"ServiceMethodArray": {"serviceMethod": [""]}})
