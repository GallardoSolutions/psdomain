import pytest
from pydantic import ValidationError

from psdomain.model.order_status.v_2_0_0 import Issue, OrderStatusDetail


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


ISSUE = {
    "issueId": "I-1", "issueStatus": "Open", "issueCategory": "Proof Hold", "issueName": "Proof",
    "urgentResponseRequired": False, "issueDescription": "Approve the proof",
    "responseRequiredBy": "2030-01-01T00:00:00+00:00", "issueResolutionURL": "https://example.com/issue/1",
    "issueBlockingStatus": "In Production",
}


def test_issue_accepts_resolutions_with_parameters():
    issue = Issue.model_validate({**ISSUE, "ResolutionArray": {"Resolution": [{
        "resolutionId": "R-1", "resolutionName": "Approve", "resolutionDescription": "Approve as is",
        "ParameterArray": {"Parameter": []},
    }]}})

    resolution = issue.ResolutionArray.Resolution[0]
    assert resolution.resolutionId == "R-1"
    assert resolution.ParameterArray is not None


@pytest.mark.parametrize("when", ["2030-01-01T00:00:00+00:00", "2030-01-01T00:00:00", "2020-01-01T00:00:00-05:00"])
def test_issue_accepts_any_response_required_by(when):
    """A deadline with or without an offset, and one already past, is the supplier's data, not an invalid answer."""
    issue = Issue.model_validate({**ISSUE, "responseRequiredBy": when})

    assert issue.responseRequiredBy.year in (2020, 2030)


def test_issue_still_rejects_a_url_that_is_not_http():
    with pytest.raises(ValidationError):
        Issue.model_validate({**ISSUE, "issueResolutionURL": "ftp://example.com/issue/1"})


def test_order_status_detail_accepts_an_issue_array():
    detail = OrderStatusDetail.model_validate(_detail(IssueArray={"Issue": [ISSUE]}))

    assert detail.IssueArray.Issue[0].issueId == "I-1"
