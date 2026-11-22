from psdomain.model.order_status.v_2_0_0 import OrderStatusDetail


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
