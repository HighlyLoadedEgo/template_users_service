import base64
import secrets
from typing import (
    Callable,
    Optional,
)

from fastapi import (
    Request,
    Response,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from src.application.api.config import AppConfig


class ApidocBasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app_config: AppConfig,
        app: ASGIApp,
        dispatch: Optional[DispatchFunction] = None,
    ) -> None:
        self._config = app_config
        super().__init__(app=app, dispatch=dispatch)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """Authenticate request at docs endpoint."""
        docs_paths = (
            self._config.doc_url,
            self._config.openapi_url,
            self._config.redoc_url,
        )
        if request.url.path in docs_paths:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                try:
                    scheme, credentials = auth_header.split()
                    if scheme.lower() == "basic":
                        decoded = base64.b64decode(credentials).decode("ascii")
                        username, password = decoded.split(":")
                        correct_username = secrets.compare_digest(
                            username, self._config.doc_username
                        )
                        correct_password = secrets.compare_digest(
                            password, self._config.doc_password
                        )
                        if correct_username and correct_password:
                            return await call_next(request)
                except Exception:
                    pass
            response = Response(content="Unauthorized", status_code=401)
            response.headers["WWW-Authenticate"] = "Basic"
            return response
        return await call_next(request)


def apidoc_auth_middleware(
    app_config: AppConfig,
) -> Callable[[ASGIApp, Optional[DispatchFunction]], ApidocBasicAuthMiddleware]:
    """Closure for apidoc-auth middleware with app config."""

    def setup_apidoc_auth_middleware(
        app: ASGIApp, dispatch: Optional[DispatchFunction] = None
    ) -> ApidocBasicAuthMiddleware:
        return ApidocBasicAuthMiddleware(
            app_config=app_config, app=app, dispatch=dispatch
        )

    return setup_apidoc_auth_middleware
