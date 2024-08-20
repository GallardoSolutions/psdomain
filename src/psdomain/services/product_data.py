from ..model import GetProductSellableResponse, ProductResponse


class ProductSellableService:
    def __init__(self, resp: GetProductSellableResponse):
        self.resp = resp

    def get_product_ids(self):
        if self.resp.is_ok:
            return {product.productId for product in self.resp.ProductSellableArray.ProductSellable}


class ProductService:
    def __init__(self, resp: ProductResponse):
        self.resp = resp
