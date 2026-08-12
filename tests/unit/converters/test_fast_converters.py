"""
Tests for the REST-only sellable fast/ids converters.

Tests roundtrip conversion: Pydantic -> Proto -> Pydantic
"""
from psdomain.model.base import ServiceMessage, Severity
from psdomain.model.product_data.fast import (
    SlimProduct, SellableFastResponse, SellableProductIdsResponse,
)
from psdomain.converters.product import fast


class TestSellableFastConverter:
    def test_roundtrip_with_variants(self):
        resp = SellableFastResponse.from_products([
            {"productId": "A", "variants": ["1", "2"], "no_variants": 2},
            {"productId": "B", "variants": [], "no_variants": 1},
        ])
        back = fast.fast_from_proto(fast.fast_to_proto(resp))
        assert back.count == 2
        assert back.products[0] == SlimProduct(productId="A", variants=["1", "2"], no_variants=2)
        assert back.products[1] == SlimProduct(productId="B", variants=[], no_variants=1)
        assert back.ServiceMessageArray is None

    def test_roundtrip_service_message(self):
        resp = SellableFastResponse.from_service_message_array(
            [ServiceMessage(code=110, description="auth", severity=Severity.ERROR)]
        )
        back = fast.fast_from_proto(fast.fast_to_proto(resp))
        assert back.count == 0
        assert back.products == []
        assert back.ServiceMessageArray.ServiceMessage[0].code == 110

    def test_empty(self):
        back = fast.fast_from_proto(fast.fast_to_proto(SellableFastResponse.from_products([])))
        assert back.count == 0
        assert back.products == []
        assert back.ServiceMessageArray is None


class TestSellableProductIdsConverter:
    def test_roundtrip_ids(self):
        resp = SellableProductIdsResponse.from_products(["A", "B", "C"])
        back = fast.ids_from_proto(fast.ids_to_proto(resp))
        assert back.count == 3
        assert back.products == ["A", "B", "C"]
        assert back.ServiceMessageArray is None

    def test_roundtrip_service_message(self):
        resp = SellableProductIdsResponse.from_service_message_array(
            [ServiceMessage(code=999, description="boom", severity=Severity.INFO)]
        )
        back = fast.ids_from_proto(fast.ids_to_proto(resp))
        assert back.count == 0
        assert back.products == []
        msg = back.ServiceMessageArray.ServiceMessage[0]
        assert msg.code == 999
        assert msg.description == "boom"
