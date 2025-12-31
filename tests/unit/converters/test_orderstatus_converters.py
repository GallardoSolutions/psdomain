"""
Tests for order status converters (v100).

Tests roundtrip conversion: JSON -> Pydantic -> Proto -> Pydantic
"""
from datetime import datetime, timezone

from psdomain.model.order_status.v_1_0_0 import (
    OrderStatusDetailsResponse,
    OrderStatusTypesResponse,
    OrderStatus,
    OrderStatusArray,
    OrderStatusDetail,
    OrderStatusDetailArray,
    RespondTo,
    ResponseToArray,
    Status,
    StatusArray,
)
from psdomain.converters.orderstatus import v100


class TestOrderStatusV100Converter:
    """Tests for Order Status v1.0.0 converter."""

    def test_basic_order_status_response(self):
        """Test basic order status response conversion."""
        # Create pydantic model directly since field names are camelCase
        order_detail = OrderStatusDetail(
            factoryOrderNumber="FACT-001",
            statusID=20,
            statusName="Order Confirmed",
            responseRequired=False,
            validTimestamp=datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
            expectedShipDate=None,
            expectedDeliveryDate=None,
            ResponseToArray=None,
            additionalExplanation=None,
        )

        order_status = OrderStatus(
            purchaseOrderNumber="PO-12345",
            OrderStatusDetailArray=OrderStatusDetailArray(OrderStatusDetail=[order_detail]),
        )

        response = OrderStatusDetailsResponse(
            OrderStatusArray=OrderStatusArray(OrderStatus=[order_status]),
            errorMessage=None,
        )

        proto_response = v100.to_proto(response)

        # Verify proto
        assert len(proto_response.order_statuses) == 1
        assert proto_response.order_statuses[0].purchase_order_number == "PO-12345"
        assert proto_response.order_statuses[0].order_status_details[0].factory_order_number == "FACT-001"
        assert proto_response.order_statuses[0].order_status_details[0].status_id == 20

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert roundtrip.OrderStatusArray.OrderStatus[0].purchaseOrderNumber == "PO-12345"
        assert roundtrip.OrderStatusArray.OrderStatus[0].OrderStatusDetailArray.OrderStatusDetail[0].statusID == 20

    def test_order_status_with_respond_to(self):
        """Test order status with respond to contact info."""
        respond_to = RespondTo(
            name="John Doe",
            emailAddress="john@example.com",
            phoneNumber="555-1234",
        )

        order_detail = OrderStatusDetail(
            factoryOrderNumber="FACT-002",
            statusID=42,
            statusName="Proof Hold",
            responseRequired=True,
            validTimestamp=datetime(2024, 2, 20, 14, 0, 0, tzinfo=timezone.utc),
            expectedShipDate=datetime(2024, 3, 1, 0, 0, 0, tzinfo=timezone.utc),
            expectedDeliveryDate=datetime(2024, 3, 5, 0, 0, 0, tzinfo=timezone.utc),
            ResponseToArray=ResponseToArray(RespondTo=[respond_to]),
            additionalExplanation="Please approve the proof",
        )

        order_status = OrderStatus(
            purchaseOrderNumber="PO-67890",
            OrderStatusDetailArray=OrderStatusDetailArray(OrderStatusDetail=[order_detail]),
        )

        response = OrderStatusDetailsResponse(
            OrderStatusArray=OrderStatusArray(OrderStatus=[order_status]),
            errorMessage=None,
        )

        proto_response = v100.to_proto(response)

        # Verify respond_to in proto
        detail = proto_response.order_statuses[0].order_status_details[0]
        assert detail.response_required is True
        assert len(detail.respond_to) == 1
        assert detail.respond_to[0].name == "John Doe"
        assert detail.respond_to[0].email_address == "john@example.com"
        assert detail.additional_explanation == "Please approve the proof"

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        rt_detail = roundtrip.OrderStatusArray.OrderStatus[0].OrderStatusDetailArray.OrderStatusDetail[0]
        assert rt_detail.ResponseToArray.RespondTo[0].name == "John Doe"
        assert rt_detail.ResponseToArray.RespondTo[0].emailAddress == "john@example.com"

    def test_order_status_with_error(self):
        """Test order status response with error message."""
        response = OrderStatusDetailsResponse(
            OrderStatusArray=None,
            errorMessage="Order not found",
        )

        proto_response = v100.to_proto(response)

        # Verify error
        assert proto_response.error_message == "Order not found"
        assert len(proto_response.order_statuses) == 0

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert roundtrip.OrderStatusArray is None
        assert roundtrip.errorMessage == "Order not found"

    def test_order_status_types_response(self):
        """Test order status types response conversion."""
        statuses = [
            Status(id=10, name="Order Received"),
            Status(id=20, name="Order Confirmed"),
            Status(id=60, name="In Production"),
            Status(id=80, name="Complete"),
        ]

        response = OrderStatusTypesResponse(
            StatusArray=StatusArray(Status=statuses),
            errorMessage=None,
        )

        proto_response = v100.order_status_types_to_proto(response)

        # Verify proto
        assert len(proto_response.status_types) == 4
        assert proto_response.status_types[0].id == 10
        assert proto_response.status_types[0].name == "Order Received"
        assert proto_response.status_types[3].id == 80

        # Roundtrip
        roundtrip = v100.order_status_types_from_proto(proto_response)
        assert len(roundtrip.StatusArray.Status) == 4
        assert roundtrip.StatusArray.Status[0].id == 10
        assert roundtrip.StatusArray.Status[3].name == "Complete"

    def test_multiple_orders(self):
        """Test response with multiple orders."""
        orders = []
        for i in range(3):
            order_detail = OrderStatusDetail(
                factoryOrderNumber=f"FACT-{i:03d}",
                statusID=20 + i * 10,
                statusName=f"Status {i}",
                responseRequired=False,
                validTimestamp=datetime(2024, 1, 1 + i, 12, 0, 0, tzinfo=timezone.utc),
                expectedShipDate=None,
                expectedDeliveryDate=None,
                ResponseToArray=None,
                additionalExplanation=None,
            )
            orders.append(OrderStatus(
                purchaseOrderNumber=f"PO-{i:05d}",
                OrderStatusDetailArray=OrderStatusDetailArray(OrderStatusDetail=[order_detail]),
            ))

        response = OrderStatusDetailsResponse(
            OrderStatusArray=OrderStatusArray(OrderStatus=orders),
            errorMessage=None,
        )

        proto_response = v100.to_proto(response)

        # Verify proto
        assert len(proto_response.order_statuses) == 3
        assert proto_response.order_statuses[0].purchase_order_number == "PO-00000"
        assert proto_response.order_statuses[2].purchase_order_number == "PO-00002"

        # Roundtrip
        roundtrip = v100.from_proto(proto_response)
        assert len(roundtrip.OrderStatusArray.OrderStatus) == 3
