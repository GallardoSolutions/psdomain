"""Converters for the REST-only sellable fast/ids responses.

    from psdomain.converters.product import fast
    proto = fast.fast_to_proto(sellable_fast_response)
    pydantic = fast.fast_from_proto(proto)

These pair with ``psdomain.model.product_data.fast`` and
``psdomain.proto.product.fast_pb2``.
"""
from psdomain.proto.product import fast_pb2 as proto
from psdomain.proto.inventory import shared_pb2 as inv_shared
from psdomain.model.base import ServiceMessage, ServiceMessageArray
from psdomain.model.product_data.fast import (
    SlimProduct, SellableFastResponse, SellableProductIdsResponse,
)


# --- ServiceMessage (shared inventory.ServiceMessage, matches v2.0.0) ---

def _sm_to_proto(m: ServiceMessage):
    return inv_shared.ServiceMessage(
        code=m.code,
        description=m.description,
        severity=str(m.severity) if m.severity else "",
    )


def _sm_from_proto(p) -> ServiceMessage:
    return ServiceMessage(
        code=p.code,
        description=p.description,
        severity=p.severity if p.severity else "Error",
    )


def _service_message_array_from_proto(msgs) -> ServiceMessageArray | None:
    if not msgs:
        return None
    return ServiceMessageArray(ServiceMessage=[_sm_from_proto(m) for m in msgs])


# --- SlimProduct ---

def slim_product_to_proto(sp: SlimProduct):
    return proto.SlimProduct(
        product_id=sp.productId,
        variants=list(sp.variants),
        no_variants=sp.no_variants,
    )


def slim_product_from_proto(p) -> SlimProduct:
    return SlimProduct(productId=p.product_id, variants=list(p.variants), no_variants=p.no_variants)


# --- SellableFastResponse (/sellables) ---

def fast_to_proto(resp: SellableFastResponse):
    result = proto.SellableFastResponse()
    for sp in resp.products:
        result.products.append(slim_product_to_proto(sp))
    if resp.ServiceMessageArray:
        for m in resp.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(_sm_to_proto(m))
    return result


def fast_from_proto(proto_msg) -> SellableFastResponse:
    products = [slim_product_from_proto(p) for p in proto_msg.products]
    return SellableFastResponse(
        count=len(products),
        products=products,
        ServiceMessageArray=_service_message_array_from_proto(proto_msg.service_messages),
    )


# --- SellableProductIdsResponse (/sellable-product-ids) ---

def ids_to_proto(resp: SellableProductIdsResponse):
    result = proto.SellableProductIdsResponse(product_ids=list(resp.products))
    if resp.ServiceMessageArray:
        for m in resp.ServiceMessageArray.ServiceMessage:
            result.service_messages.append(_sm_to_proto(m))
    return result


def ids_from_proto(proto_msg) -> SellableProductIdsResponse:
    ids = list(proto_msg.product_ids)
    return SellableProductIdsResponse(
        count=len(ids),
        products=ids,
        ServiceMessageArray=_service_message_array_from_proto(proto_msg.service_messages),
    )
