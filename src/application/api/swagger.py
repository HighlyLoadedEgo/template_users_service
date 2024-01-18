from typing import Any

from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from src.application.api.config import AppConfig
from src.application.api.security.permission_check import check_doc_permission


def init_swagger_endpoints(app: FastAPI, app_config: AppConfig) -> None:
    """Initialize swagger api with config."""
    permission_depends = check_doc_permission(app_config=app_config)

    async def get_swagger_documentation() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app_config.openapi_url, title=app_config.title
        )

    async def openapi() -> dict[str, Any]:
        return get_openapi(
            title=app_config.title, version=app_config.version, routes=app.routes
        )

    async def get_redoc() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app_config.openapi_url, title=app_config.title
        )

    app.get(
        app_config.doc_url,
        tags=["documentation"],
        include_in_schema=False,
        dependencies=[Depends(permission_depends)],
    )(get_swagger_documentation)
    app.get(
        app_config.openapi_url,
        tags=["documentation"],
        include_in_schema=False,
        dependencies=[Depends(permission_depends)],
    )(openapi)
    app.get(
        app_config.redoc_url,
        tags=["documentation"],
        include_in_schema=False,
        dependencies=[Depends(permission_depends)],
    )(get_redoc)
