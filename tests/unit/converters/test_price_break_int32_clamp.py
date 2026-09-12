"""Price-break quantities beyond int32 must be clamped, not fail the protobuf write.

2026-09-12: Aakron sends quantityMax = 9223372036854775807 (int64 max, "no upper bound") on the last
price break of product 98202. quantity_max is int32 in the proto, so the protobuf cache write failed
("Value out of range", PSRESTFUL-API-37) and the product fell back to pickle on every request.
"""
import importlib
from decimal import Decimal

import pytest

from psdomain.converters.base import INT32_MAX, int32_clamped
from psdomain.converters.product import v100, v200
from psdomain.model.product_data.common import ProductPrice

PROTO = {
    v200: importlib.import_module('psdomain.proto.product.v200_pb2'),
    v100: importlib.import_module('psdomain.proto.product.v100_pb2'),
}


@pytest.mark.parametrize('value, expected', [
    (5, 5),
    (INT32_MAX, INT32_MAX),
    (2 ** 63 - 1, INT32_MAX),
    (-2 ** 63, -INT32_MAX - 1),
    ('12', 12),
])
def test_int32_clamped(value, expected):
    assert int32_clamped(value) == expected


@pytest.mark.parametrize('module', [v200, v100])
def test_unbounded_last_break_round_trips_as_int32_max(module):
    price = ProductPrice(quantityMin=1000, quantityMax=2 ** 63 - 1, price=Decimal('1.5'), discountCode=None)

    proto = module.product_price_to_proto(price, PROTO[module])
    assert proto.quantity_max == INT32_MAX
    assert proto.quantity_min == 1000

    back = module.product_price_from_proto(proto)
    assert back.quantityMax == INT32_MAX
    assert back.price == Decimal('1.5')


@pytest.mark.parametrize('module', [v200, v100])
def test_missing_max_is_still_unset(module):
    price = ProductPrice(quantityMin=1, quantityMax=None, price=Decimal('2'), discountCode=None)
    proto = module.product_price_to_proto(price, PROTO[module])
    assert not proto.HasField('quantity_max')
    assert module.product_price_from_proto(proto).quantityMax is None
