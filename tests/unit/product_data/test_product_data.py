# flake8: noqa F811

from psdomain.model.product_data.v_2_0_0 import GetProductSellableResponseV200
from .fixtures import sellable_response  # noqa


def test_get_product_sellable_response_v200(sellable_response):
    response = GetProductSellableResponseV200.model_validate(sellable_response)

    assert response.ProductSellableArray.ProductSellable[0].productId == '0011-86'
    assert response.ProductSellableArray.ProductSellable[0].partId == '0011-86BK'
    assert response.ProductSellableArray.ProductSellable[0].culturePoint is None

    assert response.ProductSellableArray.ProductSellable[1].productId == '0022-45'
    assert response.ProductSellableArray.ProductSellable[1].partId == '0022-45BK'
    assert response.ProductSellableArray.ProductSellable[1].culturePoint is None

    assert response.ProductSellableArray.ProductSellable[2].productId == '0022-46'
    assert response.ProductSellableArray.ProductSellable[2].partId == '0022-46BK'
    assert response.ProductSellableArray.ProductSellable[2].culturePoint is None
