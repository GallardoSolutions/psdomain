# Proto generated files for product service

# V1.0.0 types
from .v100_pb2 import (
    ErrorMessage,
    GetProductRequestV100,
    GetProductResponseV100,
    GetProductCloseOutRequestV100,
    GetProductCloseOutResponseV100,
    GetProductSellableRequestV100,
    GetProductSellableResponseV100,
    GetProductDateModifiedRequestV100,
    GetProductDateModifiedResponseV100,
    ProductGroupV100,  # Shared grouped type for CloseOut, Sellable, DateModified
    ProductV100,
    ProductPartV100,
    ApparelSizeV100,
    ColorV100,
    DimensionV100,
    SpecificationV100,
    ProductPackageV100,
    ShippingPackageV100,
    ProductMarketingPointV100,
    ProductKeywordV100,
    ProductCategoryV100,
    RelatedProductV100,
    ProductPriceV100,
)

# V2.0.0 types
from .v200_pb2 import (
    GetProductRequest,
    GetProductResponse,
    GetProductCloseOutRequest,
    GetProductCloseOutResponse,
    GetProductSellableRequest,
    GetProductSellableResponse,
    GetProductDateModifiedRequest,
    GetProductDateModifiedResponse,
    ProductGroup,  # Shared grouped type for CloseOut, Sellable, DateModified
    Product,
    ProductPart,
    ApparelSize,
    Color,
    Dimension,
    Specification,
    ProductPackage,
    ShippingPackage,
    ProductMarketingPoint,
    ProductKeyword,
    ProductCategory,
    RelatedProduct,
    ProductPriceGroup,
    ProductPrice,
    LocationDecoration,
    FobPoint,
)

# gRPC service (includes both v2.0.0 and v1.0.0 RPCs)
from .v200_pb2_grpc import (
    ProductServiceStub,
    ProductServiceServicer,
    add_ProductServiceServicer_to_server,
)
