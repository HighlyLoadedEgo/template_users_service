from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)

TResult = TypeVar("TResult")
TError = TypeVar("TError")


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class OkResponse(Response, Generic[TResult]):
    status: int = 200
    result: TResult | None = None
    message: str | None = None


@dataclass(frozen=True)
class ErrorData(Generic[TError]):
    message: str = "Error message"
    data: TError | None = None


@dataclass(frozen=True)
class ErrorResponse(Response, Generic[TError]):
    error: ErrorData[TError] = field(default_factory=ErrorData)
    status: int = 500
