# flake8: noqa F811

from psdomain.model import GetProductSellableResponseV200
from tests.unit.product_data.fixtures import sellable_response  # noqa

from psdomain.services.product_data import ProductSellableService


def test_get_product_sellable_response_v200(sellable_response):
    response = GetProductSellableResponseV200.model_validate(sellable_response)

    srv = ProductSellableService(response)
    assert {"0011-86", "0022-45", "0022-46"} == srv.get_product_ids()
