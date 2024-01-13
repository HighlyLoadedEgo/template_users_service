from collections.abc import (
    Awaitable,
    Callable,
)
from functools import partial

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request

from src.application.api.responses.orjson import ORJSONResponseImpl
from src.core.auth.exceptions import (
    AccessDeniedException,
    InvalidTokenException,
)
from src.core.common import BaseAppException
from src.core.common.schemas.base_responses import (
    ErrorData,
    ErrorResponse,
)
from src.modules.users.exceptions import (
    IncorrectUserCredentialsException,
    UserDataIsExistException,
    UserDoesNotExistException,
)

# logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        BaseAppException, error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
    app.add_exception_handler(
        IncorrectUserCredentialsException, error_handler(status.HTTP_401_UNAUTHORIZED)
    )
    app.add_exception_handler(
        UserDoesNotExistException, error_handler(status.HTTP_404_NOT_FOUND)
    )
    app.add_exception_handler(
        UserDataIsExistException, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(
        AccessDeniedException, error_handler(status.HTTP_403_FORBIDDEN)
    )
    app.add_exception_handler(
        InvalidTokenException, error_handler(status.HTTP_403_FORBIDDEN)
    )
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponseImpl]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(
    request: Request, err: BaseAppException, status_code: int
) -> ORJSONResponseImpl:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(message=err.message, data=err),
        status_code=status_code,
    )


async def unknown_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponseImpl:
    # logger.error("Handle error", exc_info=err, extra={"error": err})
    # logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponseImpl(
        ErrorResponse(
            error=ErrorData(data=err), status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_data: ErrorData,
    status_code: int,
) -> ORJSONResponseImpl:
    # logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponseImpl(ErrorResponse(error=err_data, status=status_code))
