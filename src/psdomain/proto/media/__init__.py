# Proto generated files for media service

# v1.1.0 types
from .v110_pb2 import (
    ErrorMessage,
    GetMediaContentRequest,
    GetMediaContentResponse,
    GetMediaDateModifiedRequest,
    GetMediaDateModifiedResponse,
    MediaContent,
    MediaGroup,
    ClassType,
    Decoration,
    Location,
)

# gRPC service
from .v110_pb2_grpc import (
    MediaServiceStub,
    MediaServiceServicer,
    add_MediaServiceServicer_to_server,
)
