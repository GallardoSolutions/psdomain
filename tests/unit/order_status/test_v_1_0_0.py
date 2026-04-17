from psdomain.model.order_status.v_1_0_0 import (
    OrderStatusDetail,
    OrderStatusDetailsResponse,
)


def test_order_status_detail_statusname_optional():
    """PS v1.0.0 WSDL declares statusName with minOccurs=0; parsing must succeed when it is absent."""
    detail = OrderStatusDetail.model_validate({
        "factoryOrderNumber": "N/A",
        "statusID": 0,
        "statusName": None,
        "responseRequired": False,
        "validTimestamp": "1900-01-01T01:01:01+00:00",
        "expectedShipDate": None,
        "expectedDeliveryDate": None,
        "ResponseToArray": None,
        "additionalExplanation": None,
    })
    assert detail.statusName is None
    assert detail.statusID == 0


def test_hirsch_no_orders_placeholder_response():
    """Reproduces Hirsch's GetOrderStatusDetails 'No orders were found' placeholder response,
    which omits statusName on the placeholder OrderStatusDetail."""
    resp = OrderStatusDetailsResponse.model_validate({
        "OrderStatusArray": {
            "OrderStatus": [
                {
                    "purchaseOrderNumber": "N/A",
                    "OrderStatusDetailArray": {
                        "OrderStatusDetail": [
                            {
                                "factoryOrderNumber": "N/A",
                                "statusID": 0,
                                "statusName": None,
                                "expectedShipDate": None,
                                "expectedDeliveryDate": None,
                                "ResponseToArray": None,
                                "additionalExplanation": None,
                                "responseRequired": False,
                                "validTimestamp": "1900-01-01T01:01:01+00:00",
                            }
                        ]
                    },
                }
            ]
        },
        "errorMessage": "No orders were found",
    })
    assert resp.errorMessage == "No orders were found"
    detail = resp.OrderStatusArray.OrderStatus[0].OrderStatusDetailArray.OrderStatusDetail[0]
    assert detail.statusName is None
