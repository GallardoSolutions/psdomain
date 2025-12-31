"""
Media Content v1.1.0 converters.

Converts between pydantic MediaContentDetailsResponse and proto GetMediaContentResponse.
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from psdomain.converters.base import proto_str_or_none, pydantic_str_or_empty
from psdomain.model.base import ServiceMessage, ServiceMessageArray
from psdomain.model.media_content import (
    ClassType,
    Decoration,
    Location,
    MediaContent,
    MediaContentDetailsResponse,
    MediaDateModified,
)

if TYPE_CHECKING:
    from psdomain.proto.media import v110_pb2 as proto


def _get_proto():
    """Lazy import of proto module."""
    from psdomain.proto.media import v110_pb2
    return v110_pb2


# --- Helper converters for nested types ---


def decoration_to_proto(dec: Decoration) -> "proto.Decoration":
    """Convert pydantic Decoration to proto Decoration."""
    pb2 = _get_proto()
    return pb2.Decoration(
        decoration_id=pydantic_str_or_empty(dec.decorationId),
        decoration_name=pydantic_str_or_empty(dec.decorationName),
    )


def decoration_from_proto(p: "proto.Decoration") -> Decoration:
    """Convert proto Decoration to pydantic Decoration."""
    return Decoration(
        decorationId=proto_str_or_none(p.decoration_id),
        decorationName=proto_str_or_none(p.decoration_name),
    )


def location_to_proto(loc: Location) -> "proto.Location":
    """Convert pydantic Location to proto Location."""
    pb2 = _get_proto()
    return pb2.Location(
        location_id=loc.locationId or 0,
        location_name=pydantic_str_or_empty(loc.locationName),
    )


def location_from_proto(p: "proto.Location") -> Location:
    """Convert proto Location to pydantic Location."""
    return Location(
        locationId=p.location_id if p.location_id else None,
        locationName=proto_str_or_none(p.location_name),
    )


def class_type_to_proto(ct: ClassType | None) -> str:
    """Convert pydantic ClassType enum to proto string."""
    if ct is None:
        return ""
    return ct.value


def class_type_from_proto(value: str) -> ClassType | None:
    """Convert proto string to pydantic ClassType enum."""
    if not value:
        return None
    try:
        return ClassType(value)
    except ValueError:
        return None


# --- MediaContent converters ---


def media_content_to_proto(mc: MediaContent) -> "proto.MediaContent":
    """Convert pydantic MediaContent to proto MediaContent."""
    pb2 = _get_proto()
    result = pb2.MediaContent(
        product_id=pydantic_str_or_empty(mc.productId),
        part_id=pydantic_str_or_empty(mc.partId),
        url=pydantic_str_or_empty(mc.url),
        media_type=pydantic_str_or_empty(mc.mediaType),
        class_type=class_type_to_proto(mc.classType),
        file_size=pydantic_str_or_empty(mc.fileSize),
        height=pydantic_str_or_empty(mc.height),
        width=pydantic_str_or_empty(mc.width),
        dpi=pydantic_str_or_empty(mc.dpi),
        color=pydantic_str_or_empty(mc.color),
        description=pydantic_str_or_empty(mc.description),
        single_part=mc.singlePart if mc.singlePart is not None else False,
        change_time=pydantic_str_or_empty(mc.changeTime),
    )
    if mc.Decoration:
        result.decoration.CopyFrom(decoration_to_proto(mc.Decoration))
    if mc.Location:
        result.location.CopyFrom(location_to_proto(mc.Location))
    return result


def media_content_from_proto(p: "proto.MediaContent") -> MediaContent:
    """Convert proto MediaContent to pydantic MediaContent."""
    decoration = None
    if p.HasField("decoration"):
        decoration = decoration_from_proto(p.decoration)

    location = None
    if p.HasField("location"):
        location = location_from_proto(p.location)

    return MediaContent(
        productId=proto_str_or_none(p.product_id),
        partId=proto_str_or_none(p.part_id),
        url=proto_str_or_none(p.url),
        mediaType=proto_str_or_none(p.media_type),
        classType=class_type_from_proto(p.class_type),
        fileSize=proto_str_or_none(p.file_size),
        height=proto_str_or_none(p.height),
        width=proto_str_or_none(p.width),
        dpi=proto_str_or_none(p.dpi),
        color=proto_str_or_none(p.color),
        description=proto_str_or_none(p.description),
        singlePart=p.single_part if p.single_part else None,
        changeTime=proto_str_or_none(p.change_time),
        Decoration=decoration,
        Location=location,
    )


# --- MediaDateModified / MediaGroup converters ---


def media_date_modified_to_proto_groups(
    items: list[MediaDateModified],
) -> list["proto.MediaGroup"]:
    """Convert list of MediaDateModified to list of MediaGroup.

    Groups by productId with list of partIds.
    """
    pb2 = _get_proto()
    # Group by productId
    groups: dict[str, list[str]] = defaultdict(list)
    for item in items:
        product_id = item.productId or ""
        part_id = item.partId or ""
        if part_id:
            groups[product_id].append(part_id)
        elif product_id and product_id not in groups:
            groups[product_id] = []

    result = []
    for product_id, part_ids in groups.items():
        result.append(
            pb2.MediaGroup(
                product_id=product_id,
                part_ids=part_ids,
            )
        )
    return result


def media_groups_from_proto(
    groups: list["proto.MediaGroup"],
) -> list[MediaDateModified]:
    """Convert list of MediaGroup to list of MediaDateModified.

    Expands groups back to individual (productId, partId) pairs.
    """
    result = []
    for group in groups:
        if group.part_ids:
            for part_id in group.part_ids:
                result.append(
                    MediaDateModified(
                        productId=proto_str_or_none(group.product_id),
                        partId=proto_str_or_none(part_id),
                    )
                )
        else:
            # Product without parts
            result.append(
                MediaDateModified(
                    productId=proto_str_or_none(group.product_id),
                    partId=None,
                )
            )
    return result


# --- ServiceMessage converters ---


def service_message_to_proto(msg: ServiceMessage) -> "proto.ServiceMessage":
    """Convert pydantic ServiceMessage to proto ServiceMessage."""
    pb2 = _get_proto()
    return pb2.ServiceMessage(
        code=msg.code or 0,
        description=pydantic_str_or_empty(msg.description),
        severity=str(msg.severity) if msg.severity else "",
    )


def service_message_from_proto(p: "proto.ServiceMessage") -> ServiceMessage:
    """Convert proto ServiceMessage to pydantic ServiceMessage."""
    return ServiceMessage(
        code=p.code if p.code else None,
        description=proto_str_or_none(p.description),
        severity=proto_str_or_none(p.severity),
    )


# --- Main response converters ---


def to_proto(
    response: MediaContentDetailsResponse,
) -> "proto.GetMediaContentResponse":
    """Convert pydantic MediaContentDetailsResponse to proto GetMediaContentResponse."""
    pb2 = _get_proto()
    result = pb2.GetMediaContentResponse()

    if response.MediaContent:
        for mc in response.MediaContent:
            result.media_content.append(media_content_to_proto(mc))

    if response.ServiceMessageArray and response.ServiceMessageArray.ServiceMessage:
        for msg in response.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(service_message_to_proto(msg))

    return result


def from_proto(
    proto_msg: "proto.GetMediaContentResponse",
) -> MediaContentDetailsResponse:
    """Convert proto GetMediaContentResponse to pydantic MediaContentDetailsResponse."""
    media_content = None
    if proto_msg.media_content:
        media_content = [
            media_content_from_proto(mc) for mc in proto_msg.media_content
        ]

    service_messages = None
    if proto_msg.service_messages:
        msgs = [service_message_from_proto(m) for m in proto_msg.service_messages]
        service_messages = ServiceMessageArray(ServiceMessage=msgs)

    return MediaContentDetailsResponse(
        MediaContent=media_content,
        MediaDateModified=None,
        ServiceMessageArray=service_messages,
    )


# --- GetMediaDateModifiedResponse converters ---


def date_modified_to_proto(
    response: MediaContentDetailsResponse,
) -> "proto.GetMediaDateModifiedResponse":
    """Convert pydantic MediaContentDetailsResponse to proto GetMediaDateModifiedResponse.

    Uses MediaDateModified field instead of MediaContent.
    """
    pb2 = _get_proto()
    result = pb2.GetMediaDateModifiedResponse()

    if response.MediaDateModified:
        result.media_groups.extend(
            media_date_modified_to_proto_groups(response.MediaDateModified)
        )

    if response.ServiceMessageArray and response.ServiceMessageArray.ServiceMessage:
        for msg in response.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(service_message_to_proto(msg))

    return result


def date_modified_from_proto(
    proto_msg: "proto.GetMediaDateModifiedResponse",
) -> MediaContentDetailsResponse:
    """Convert proto GetMediaDateModifiedResponse to pydantic MediaContentDetailsResponse.

    Populates MediaDateModified field instead of MediaContent.
    """
    media_date_modified = None
    if proto_msg.media_groups:
        media_date_modified = media_groups_from_proto(list(proto_msg.media_groups))

    service_messages = None
    if proto_msg.service_messages:
        msgs = [service_message_from_proto(m) for m in proto_msg.service_messages]
        service_messages = ServiceMessageArray(ServiceMessage=msgs)

    return MediaContentDetailsResponse(
        MediaContent=None,
        MediaDateModified=media_date_modified,
        ServiceMessageArray=service_messages,
    )
