# Proto generated files for inventory service
# Shared types
from .shared_pb2 import Credentials, ServiceMessage

# V1.2.1 types (messages only - RPC is in InventoryService)
from .v121_pb2 import (
    FilterV121,
    GetInventoryLevelsRequestV121,
    GetInventoryLevelsResponseV121,
    GetFilterValuesRequestV121,
    GetFilterValuesResponseV121,
    FilterValuesV121,
    InventoryV121,
    AttributeFlex,
    ProductVariationInventory,
    ProductCompanionInventory,
)

# V2.0.0 types
from .v200_pb2 import (
    GetInventoryLevelsRequest,
    GetInventoryLevelsResponse,
    GetFilterValuesRequest,
    GetFilterValuesResponse,
    Inventory,
    PartInventory,
    QuantityAvailable,
    InventoryLocation,
    FutureAvailability,
    Filter,
    FilterValues,
)

# gRPC service (includes both v2.0.0 and v1.2.1 RPCs)
from .v200_pb2_grpc import (
    InventoryServiceStub,
    InventoryServiceServicer,
    add_InventoryServiceServicer_to_server,
)
