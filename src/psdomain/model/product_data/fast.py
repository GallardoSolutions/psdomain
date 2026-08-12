"""REST-only aggregated views derived from GetProductSellable.

These are not PromoStandards SOAP/gRPC shapes — they are the lighter payloads
the psrestful REST API serves from a single cached GetProductSellableResponse
(the ``/sellables`` and ``/sellable-product-ids`` endpoints). They live here so
both the REST layer and the protobuf converters share one canonical definition.
"""
from .. import base


class SlimProduct(base.PSBaseModel):
    productId: str
    variants: list[str]
    no_variants: int


class SellableFastResponse(base.PSBaseModel):
    """``/sellables`` payload: products grouped with their variants."""
    count: int
    products: list[SlimProduct]
    ServiceMessageArray: base.ServiceMessageArray | None = None

    @classmethod
    def from_products(cls, products) -> "SellableFastResponse":
        return cls(count=len(products), products=products, ServiceMessageArray=None)

    @classmethod
    def from_service_message_array(cls, service_message_array) -> "SellableFastResponse":
        return cls(count=0, products=[],
                   ServiceMessageArray=_to_service_message_array(service_message_array))


class SellableProductIdsResponse(base.PSBaseModel):
    """``/sellable-product-ids`` payload: the distinct product ids only."""
    count: int
    products: list[str]
    ServiceMessageArray: base.ServiceMessageArray | None = None

    @classmethod
    def from_products(cls, product_ids) -> "SellableProductIdsResponse":
        product_ids = list(product_ids)
        return cls(count=len(product_ids), products=product_ids, ServiceMessageArray=None)

    @classmethod
    def from_service_message_array(cls, service_message_array) -> "SellableProductIdsResponse":
        return cls(count=0, products=[],
                   ServiceMessageArray=_to_service_message_array(service_message_array))


def _to_service_message_array(service_message_array) -> base.ServiceMessageArray | None:
    if not service_message_array:
        return None
    messages = [
        base.ServiceMessage(code=m.code, description=m.description, severity=m.severity)
        for m in service_message_array
    ]
    return base.ServiceMessageArray(ServiceMessage=messages)
