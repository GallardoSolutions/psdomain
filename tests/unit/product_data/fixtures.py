import pytest

from psdomain.model import ProductResponseV200

from .responses.products import resp01940E1 as resp01940E1_dict

null = None


@pytest.fixture
def sellable_response():
    return {
        "ProductSellableArray": {
            "ProductSellable": [
                {
                    "productId": "0011-86",
                    "partId": "0011-86BK",
                    "culturePoint": null
                },
                {
                    "productId": "0022-45",
                    "partId": "0022-45BK",
                    "culturePoint": null
                },
                {
                    "productId": "0022-46",
                    "partId": "0022-46BK",
                    "culturePoint": null
                }
            ]
        },
        "ServiceMessageArray": null
    }


@pytest.fixture
def resp_alpha():
    yield ProductResponseV200.model_validate(resp01940E1_dict)
