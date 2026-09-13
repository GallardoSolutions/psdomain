"""lead_time, unspsc_commodity_code and max_imprint_colors are int32 in the proto and must be clamped.

Follow-up to the price-break clamp (v0.1.40): a supplier sending an out-of-range whole number in any of
these fields would make the protobuf cache write fail ("Value out of range") and force the pickle fallback.
"""
import importlib

import pytest

from psdomain.converters.base import INT32_MAX
from psdomain.converters.product import v100, v200
from psdomain.model.product_data.common import LocationDecoration
from psdomain.model.product_data.v_1_0_0 import ProductResponseV100
from psdomain.model.product_data.v_2_0_0 import ProductResponseV200

PROTO = {
    v200: importlib.import_module('psdomain.proto.product.v200_pb2'),
    v100: importlib.import_module('psdomain.proto.product.v100_pb2'),
}
RESPONSE = {v200: ProductResponseV200, v100: ProductResponseV100}
TOO_BIG = 2 ** 63 - 1


def _part(lead_time):
    return {
        'partId': 'PART-A', 'description': ['Part A'], 'countryOfOrigin': None, 'ColorArray': None,
        'primaryMaterial': None, 'SpecificationArray': None, 'shape': None, 'ApparelSize': None,
        'Dimension': None, 'leadTime': lead_time, 'unspsc': None, 'gtin': None, 'isRushService': None,
        'ProductPackagingArray': None, 'ShippingPackageArray': None, 'endDate': None, 'effectiveDate': None,
        'isCloseout': None, 'isCaution': None, 'cautionComment': None, 'nmfcCode': None,
        'nmfcDescription': None, 'nmfcNumber': None, 'isOnDemand': None, 'isHazmat': None,
    }


def _response(module, lead_time=None, unspsc_commodity_code=None, max_imprint_colors=None):
    product = {
        'productId': 'P-1', 'productName': 'Product', 'ProductCategoryArray': None, 'RelatedProductArray': None,
        'ProductKeywordArray': None, 'ProductMarketingPointArray': None,
        'ProductPartArray': {'ProductPart': [_part(lead_time)]}, 'unspscCommodityCode': unspsc_commodity_code,
    }
    envelope = {'ServiceMessageArray': None} if module is v200 else {'ErrorMessage': None}
    if module is v200:
        product['LocationDecorationArray'] = {'LocationDecoration': [
            {'locationName': 'Front', 'maxImprintColors': max_imprint_colors},
        ]}
        product['ProductPriceGroupArray'] = None
        product['FobPointArray'] = None
    return RESPONSE[module].model_validate({'Product': product, **envelope})


@pytest.mark.parametrize('module', [v200, v100])
def test_lead_time_is_clamped(module):
    proto = module.to_proto(_response(module, lead_time=TOO_BIG))
    assert proto.product.parts[0].lead_time == INT32_MAX
    assert module.from_proto(proto).Product.ProductPartArray.ProductPart[0].leadTime == INT32_MAX


@pytest.mark.parametrize('module', [v200, v100])
def test_missing_lead_time_stays_unset(module):
    proto = module.to_proto(_response(module, lead_time=None))
    assert not proto.product.parts[0].HasField('lead_time')
    assert module.from_proto(proto).Product.ProductPartArray.ProductPart[0].leadTime is None


def test_unspsc_commodity_code_is_clamped():
    proto = v200.to_proto(_response(v200, unspsc_commodity_code=TOO_BIG))
    assert proto.product.unspsc_commodity_code == INT32_MAX
    assert v200.from_proto(proto).Product.unspscCommodityCode == INT32_MAX


def test_missing_unspsc_commodity_code_stays_unset():
    proto = v200.to_proto(_response(v200))
    assert not proto.product.HasField('unspsc_commodity_code')
    assert v200.from_proto(proto).Product.unspscCommodityCode is None


def test_max_imprint_colors_is_clamped():
    ld = LocationDecoration(locationName='Front', maxImprintColors=TOO_BIG)
    proto = v200.location_decoration_to_proto(ld, PROTO[v200])
    assert proto.max_imprint_colors == INT32_MAX
    assert v200.location_decoration_from_proto(proto).maxImprintColors == INT32_MAX


def test_max_imprint_colors_round_trips_through_product():
    proto = v200.to_proto(_response(v200, max_imprint_colors=TOO_BIG))
    decorations = proto.product.location_decorations
    assert decorations[0].max_imprint_colors == INT32_MAX
    back = v200.from_proto(proto).Product.LocationDecorationArray.LocationDecoration[0]
    assert back.maxImprintColors == INT32_MAX


def test_missing_max_imprint_colors_stays_unset():
    proto = v200.location_decoration_to_proto(LocationDecoration(locationName='Front'), PROTO[v200])
    assert not proto.HasField('max_imprint_colors')
    assert v200.location_decoration_from_proto(proto).maxImprintColors is None
