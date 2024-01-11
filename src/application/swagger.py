from typing import Any

from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from src.application.api.config import AppConfig


def init_swagger_endpoints(app: FastAPI, app_config: AppConfig) -> None:
    """Initialize swagger endpoints with config."""

    async def get_swagger_documentation() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=app_config.openapi_url, title=app_config.doc_title
        )

    async def openapi() -> dict[str, Any]:
        return get_openapi(
            title=app_config.title, version=app_config.version, routes=app.routes
        )

    async def get_redoc() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=app_config.openapi_url, title=app_config.doc_title
        )

    app.get(
        app_config.doc_url,
        tags=["documentation"],
        include_in_schema=False,
    )(get_swagger_documentation)
    app.get(
        app_config.openapi_url,
        tags=["documentation"],
        include_in_schema=False,
    )(openapi)
    app.get(
        app_config.redoc_url,
        tags=["documentation"],
        include_in_schema=False,
    )(get_redoc)
