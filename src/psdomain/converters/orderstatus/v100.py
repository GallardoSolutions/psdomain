"""
Order Status v1.0.0 converters.

Converts between pydantic OrderStatusDetailsResponse and proto GetOrderStatusDetailsResponse.
Also handles OrderStatusTypesResponse and GetOrderStatusTypesResponse.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty
from psdomain.model.base import ErrorMessage
from psdomain.model.order_status.v_1_0_0 import (
    OrderStatus,
    OrderStatusArray,
    OrderStatusDetail,
    OrderStatusDetailArray,
    OrderStatusDetailsResponse,
    OrderStatusTypesResponse,
    RespondTo,
    ResponseToArray,
    Status,
    StatusArray,
)

if TYPE_CHECKING:
    from psdomain.proto.orderstatus import orderstatus_pb2 as proto


def _get_proto():
    """Lazy import of proto module."""
    from psdomain.proto.orderstatus import orderstatus_pb2
    return orderstatus_pb2


# --- Timestamp helpers ---


def _get_timestamp_class():
    """Lazy import of Timestamp class."""
    from google.protobuf.timestamp_pb2 import Timestamp
    return Timestamp


def datetime_to_proto(dt: datetime | None):
    """Convert datetime to proto Timestamp."""
    if dt is None:
        return None
    Timestamp = _get_timestamp_class()
    ts = Timestamp()
    ts.FromDatetime(dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc))
    return ts


def datetime_from_proto(ts) -> datetime | None:
    """Convert proto Timestamp to datetime."""
    if ts is None:
        return None
    try:
        return ts.ToDatetime(tzinfo=timezone.utc)
    except Exception:
        return None


# --- RespondTo converters ---


def respond_to_to_proto(rt: RespondTo) -> "proto.RespondTo":
    """Convert pydantic RespondTo to proto RespondTo."""
    pb2 = _get_proto()
    return pb2.RespondTo(
        name=pydantic_str_or_empty(rt.name),
        email_address=pydantic_str_or_empty(rt.emailAddress),
        phone_number=pydantic_str_or_empty(rt.phoneNumber),
    )


def respond_to_from_proto(p: "proto.RespondTo") -> RespondTo:
    """Convert proto RespondTo to pydantic RespondTo."""
    return RespondTo(
        name=proto_str_or_none(p.name),
        emailAddress=proto_str_or_none(p.email_address),
        phoneNumber=proto_str_or_none(p.phone_number),
    )


# --- OrderStatusDetail converters ---


def order_status_detail_to_proto(
    osd: OrderStatusDetail,
) -> "proto.OrderStatusDetailV100":
    """Convert pydantic OrderStatusDetail to proto OrderStatusDetailV100."""
    pb2 = _get_proto()
    result = pb2.OrderStatusDetailV100(
        factory_order_number=pydantic_str_or_empty(osd.factoryOrderNumber),
        status_id=osd.statusID,
        status_name=pydantic_str_or_empty(osd.statusName),
        response_required=osd.responseRequired if osd.responseRequired is not None else False,
        additional_explanation=pydantic_str_or_empty(osd.additionalExplanation),
    )

    # Set valid_timestamp (required)
    if osd.validTimestamp:
        ts = datetime_to_proto(osd.validTimestamp)
        if ts:
            result.valid_timestamp.CopyFrom(ts)

    # Set optional timestamps
    if osd.expectedShipDate:
        ts = datetime_to_proto(osd.expectedShipDate)
        if ts:
            result.expected_ship_date.CopyFrom(ts)

    if osd.expectedDeliveryDate:
        ts = datetime_to_proto(osd.expectedDeliveryDate)
        if ts:
            result.expected_delivery_date.CopyFrom(ts)

    # Set respond_to array
    if osd.ResponseToArray and osd.ResponseToArray.RespondTo:
        for rt in osd.ResponseToArray.RespondTo:
            result.respond_to.append(respond_to_to_proto(rt))

    return result


def order_status_detail_from_proto(
    p: "proto.OrderStatusDetailV100",
) -> OrderStatusDetail:
    """Convert proto OrderStatusDetailV100 to pydantic OrderStatusDetail."""
    respond_to_array = None
    if p.respond_to:
        respond_to_array = ResponseToArray(
            RespondTo=[respond_to_from_proto(rt) for rt in p.respond_to]
        )

    expected_ship_date = None
    if p.HasField("expected_ship_date"):
        expected_ship_date = datetime_from_proto(p.expected_ship_date)

    expected_delivery_date = None
    if p.HasField("expected_delivery_date"):
        expected_delivery_date = datetime_from_proto(p.expected_delivery_date)

    valid_timestamp = datetime_from_proto(p.valid_timestamp)
    # valid_timestamp is required, but ensure we have a fallback
    if valid_timestamp is None:
        valid_timestamp = datetime.now(tz=timezone.utc)

    return OrderStatusDetail(
        factoryOrderNumber=p.factory_order_number,
        statusID=p.status_id,
        statusName=p.status_name if p.HasField("status_name") else "",
        responseRequired=p.response_required if p.HasField("response_required") else None,
        validTimestamp=valid_timestamp,
        expectedShipDate=expected_ship_date,
        expectedDeliveryDate=expected_delivery_date,
        ResponseToArray=respond_to_array,
        additionalExplanation=(
            proto_str_or_none(p.additional_explanation) if p.HasField("additional_explanation") else None
        ),
    )


# --- OrderStatus converters ---


def order_status_to_proto(os: OrderStatus) -> "proto.OrderStatusV100":
    """Convert pydantic OrderStatus to proto OrderStatusV100."""
    pb2 = _get_proto()
    result = pb2.OrderStatusV100(
        purchase_order_number=pydantic_str_or_empty(os.purchaseOrderNumber),
    )

    if os.OrderStatusDetailArray and os.OrderStatusDetailArray.OrderStatusDetail:
        for detail in os.OrderStatusDetailArray.OrderStatusDetail:
            result.order_status_details.append(order_status_detail_to_proto(detail))

    return result


def order_status_from_proto(p: "proto.OrderStatusV100") -> OrderStatus:
    """Convert proto OrderStatusV100 to pydantic OrderStatus."""
    details = None
    if p.order_status_details:
        details = OrderStatusDetailArray(
            OrderStatusDetail=[
                order_status_detail_from_proto(d) for d in p.order_status_details
            ]
        )

    return OrderStatus(
        purchaseOrderNumber=p.purchase_order_number,
        OrderStatusDetailArray=details or OrderStatusDetailArray(OrderStatusDetail=[]),
    )


# --- Status/StatusType converters ---


def status_to_proto(s: Status) -> "proto.StatusType":
    """Convert pydantic Status to proto StatusType."""
    pb2 = _get_proto()
    return pb2.StatusType(
        id=s.id,
        name=s.name,
    )


def status_from_proto(p: "proto.StatusType") -> Status:
    """Convert proto StatusType to pydantic Status."""
    return Status(
        id=p.id,
        name=p.name,
    )


# --- Main response converters ---


def to_proto(
    response: OrderStatusDetailsResponse,
) -> "proto.GetOrderStatusDetailsResponse":
    """Convert pydantic OrderStatusDetailsResponse to proto GetOrderStatusDetailsResponse."""
    pb2 = _get_proto()
    result = pb2.GetOrderStatusDetailsResponse()

    if response.OrderStatusArray and response.OrderStatusArray.OrderStatus:
        for os in response.OrderStatusArray.OrderStatus:
            result.order_statuses.append(order_status_to_proto(os))

    if response.errorMessage:
        if isinstance(response.errorMessage, ErrorMessage):
            result.error_message = pydantic_str_or_empty(response.errorMessage.description)
        else:
            result.error_message = pydantic_str_or_empty(response.errorMessage)

    return result


def from_proto(
    proto_msg: "proto.GetOrderStatusDetailsResponse",
) -> OrderStatusDetailsResponse:
    """Convert proto GetOrderStatusDetailsResponse to pydantic OrderStatusDetailsResponse."""
    order_status_array = None
    if proto_msg.order_statuses:
        order_status_array = OrderStatusArray(
            OrderStatus=[order_status_from_proto(os) for os in proto_msg.order_statuses]
        )

    error_message = None
    if proto_msg.HasField("error_message") and proto_msg.error_message:
        error_message = proto_msg.error_message

    return OrderStatusDetailsResponse(
        OrderStatusArray=order_status_array,
        errorMessage=error_message,
    )


# --- OrderStatusTypesResponse converters ---


def order_status_types_to_proto(
    response: OrderStatusTypesResponse,
) -> "proto.GetOrderStatusTypesResponse":
    """Convert pydantic OrderStatusTypesResponse to proto GetOrderStatusTypesResponse."""
    pb2 = _get_proto()
    result = pb2.GetOrderStatusTypesResponse()

    if response.StatusArray and response.StatusArray.Status:
        for s in response.StatusArray.Status:
            result.status_types.append(status_to_proto(s))

    if response.errorMessage:
        result.error_message = pydantic_str_or_empty(response.errorMessage)

    return result


def order_status_types_from_proto(
    proto_msg: "proto.GetOrderStatusTypesResponse",
) -> OrderStatusTypesResponse:
    """Convert proto GetOrderStatusTypesResponse to pydantic OrderStatusTypesResponse."""
    status_array = None
    if proto_msg.status_types:
        status_array = StatusArray(
            Status=[status_from_proto(s) for s in proto_msg.status_types]
        )

    error_message = None
    if proto_msg.HasField("error_message") and proto_msg.error_message:
        error_message = proto_msg.error_message

    return OrderStatusTypesResponse(
        StatusArray=status_array,
        errorMessage=error_message,
    )
