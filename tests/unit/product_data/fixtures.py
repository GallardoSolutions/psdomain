import pytest

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
