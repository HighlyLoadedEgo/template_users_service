from typing import (
    ClassVar,
    Generic,
    TypeVar,
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

TResult = TypeVar("TResult")
TError = TypeVar("TError")


class Response(BaseModel):
    config_model: ClassVar = ConfigDict(frozen=True, arbitrary_types_allowed=True)


class OkResponse(Response, Generic[TResult]):
    status: int = 200
    result: TResult | None = None
    message: str | None = None


class ErrorData(Response, Generic[TError]):
    message: str = "Error message"
    data: TError | None = None


class ErrorResponse(Response, Generic[TError]):
    error: ErrorData[TError] = Field(default_factory=ErrorData)
    status: int = 500
