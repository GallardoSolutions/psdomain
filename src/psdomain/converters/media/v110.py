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
    ClassTypeArray,
    Decoration,
    DecorationArray,
    Location,
    LocationArray,
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
        decoration_id=dec.decorationId or 0,
        decoration_name=pydantic_str_or_empty(dec.decorationName),
    )


def decoration_from_proto(p: "proto.Decoration") -> Decoration:
    """Convert proto Decoration to pydantic Decoration."""
    return Decoration(
        decorationId=p.decoration_id if p.decoration_id else None,
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


def class_type_to_proto(ct: ClassType) -> "proto.ClassType":
    """Convert pydantic ClassType to proto ClassType."""
    pb2 = _get_proto()
    return pb2.ClassType(
        class_type_id=ct.classTypeId or 0,
        class_type_name=pydantic_str_or_empty(ct.classTypeName),
    )


def class_type_from_proto(p: "proto.ClassType") -> ClassType:
    """Convert proto ClassType to pydantic ClassType."""
    return ClassType(
        classTypeId=p.class_type_id if p.class_type_id else 0,
        classTypeName=proto_str_or_none(p.class_type_name) or "",
    )


# --- MediaContent converters ---


def media_content_to_proto(mc: MediaContent) -> "proto.MediaContent":
    """Convert pydantic MediaContent to proto MediaContent."""
    pb2 = _get_proto()
    result = pb2.MediaContent(
        product_id=pydantic_str_or_empty(mc.productId),
        part_id=pydantic_str_or_empty(mc.partId),
        url=pydantic_str_or_empty(mc.url),
        media_type=pydantic_str_or_empty(mc.mediaType),
        single_part=mc.singlePart if mc.singlePart is not None else False,
        color=pydantic_str_or_empty(mc.color),
        description=pydantic_str_or_empty(mc.description),
    )

    # Handle optional numeric fields
    if mc.fileSize is not None:
        result.file_size = mc.fileSize
    if mc.width is not None:
        result.width = float(mc.width)
    if mc.height is not None:
        result.height = float(mc.height)
    if mc.dpi is not None:
        result.dpi = mc.dpi

    # Convert ClassTypeArray to repeated class_types
    if mc.ClassTypeArray and mc.ClassTypeArray.ClassType:
        for ct in mc.ClassTypeArray.ClassType:
            result.class_types.append(class_type_to_proto(ct))

    # Convert DecorationArray to repeated decorations
    if mc.DecorationArray and mc.DecorationArray.Decoration:
        for dec in mc.DecorationArray.Decoration:
            result.decorations.append(decoration_to_proto(dec))

    # Convert LocationArray to repeated locations
    if mc.LocationArray and mc.LocationArray.Location:
        for loc in mc.LocationArray.Location:
            result.locations.append(location_to_proto(loc))

    return result


def media_content_from_proto(p: "proto.MediaContent") -> MediaContent:
    """Convert proto MediaContent to pydantic MediaContent."""
    # Build ClassTypeArray from repeated class_types
    class_type_array = ClassTypeArray(
        ClassType=[class_type_from_proto(ct) for ct in p.class_types]
    ) if p.class_types else ClassTypeArray(ClassType=[])

    # Build DecorationArray from repeated decorations
    decoration_array = None
    if p.decorations:
        decoration_array = DecorationArray(
            Decoration=[decoration_from_proto(dec) for dec in p.decorations]
        )

    # Build LocationArray from repeated locations
    location_array = None
    if p.locations:
        location_array = LocationArray(
            Location=[location_from_proto(loc) for loc in p.locations]
        )

    return MediaContent(
        productId=proto_str_or_none(p.product_id),
        partId=proto_str_or_none(p.part_id),
        url=proto_str_or_none(p.url),
        mediaType=proto_str_or_none(p.media_type),
        fileSize=p.file_size if p.file_size else None,
        width=int(p.width) if p.width else None,
        height=int(p.height) if p.height else None,
        dpi=p.dpi if p.dpi else None,
        color=proto_str_or_none(p.color),
        description=proto_str_or_none(p.description),
        singlePart=p.single_part,
        changeTimeStamp=None,
        ClassTypeArray=class_type_array,
        DecorationArray=decoration_array,
        LocationArray=location_array,
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
