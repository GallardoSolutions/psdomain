# flake8: noqa F811

from psdomain.model.product_data.v_2_0_0 import GetProductSellableResponseV200, ProductCloseOutResponseV200, \
    ProductDateModifiedResponseV200, ProductResponseV200
from psdomain.model.product_data.v_1_0_0 import ProductCloseOutResponseV100, ProductDateModifiedResponseV100, \
    GetProductSellableResponseV100, ProductResponseV100
from psdomain.model.base import Severity # noqa
from .fixtures import sellable_response  # noqa


def test_get_product_sellable_response_v200(sellable_response):
    response = GetProductSellableResponseV200.model_validate(sellable_response)

    arr = response.ProductSellableArray.ProductSellable

    assert arr[0].productId == '0011-86'
    assert arr[0].partId == '0011-86BK'
    assert arr[0].culturePoint is None

    assert arr[1].productId == '0022-45'
    assert arr[1].partId == '0022-45BK'
    assert arr[1].culturePoint is None

    assert arr[2].productId == '0022-46'
    assert arr[2].partId == '0022-46BK'
    assert arr[2].culturePoint is None


def test_not_supported_v200():
    classes = [ProductResponseV200, ProductCloseOutResponseV200, ProductDateModifiedResponseV200,
               GetProductSellableResponseV200]
    for cls in classes:
        resp = cls.not_supported()
        assert resp.is_ok is False
        msg = resp.ServiceMessageArray.ServiceMessage[0]
        assert msg.code == 125
        assert msg.description == 'Not Supported'
        assert msg.severity == Severity.ERROR


def test_not_supported_v100():
    classes = [ProductResponseV100, ProductCloseOutResponseV100, ProductDateModifiedResponseV100,
               GetProductSellableResponseV100]
    for cls in classes:
        resp = cls.not_supported()
        assert resp.is_ok is False
        msg = resp.ErrorMessage
        assert msg.code == 125
        assert msg.description == 'Not Supported'
