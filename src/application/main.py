import uvicorn
from fastapi import FastAPI

from src.application.api.config import (
    AppConfig,
    ServerConfig,
)
from src.application.api.exception_handler import setup_exception_handlers
from src.application.api.swagger import init_swagger_endpoints
from src.application.middlewares.main import init_middlewares


def init_app(app_config: AppConfig) -> FastAPI:
    """Initialize the FastAPI application with all dependencies."""
    app = FastAPI(
        debug=app_config.debug, doc_url=None, openapi_url=None, redoc_url=None
    )
    init_swagger_endpoints(app=app, app_config=app_config)
    init_middlewares(app=app, app_config=app_config)
    setup_exception_handlers(app=app)
    return app


async def run_api(app: FastAPI, config: ServerConfig) -> None:
    """Start the FastAPI application and uvicorn."""
    uvicorn_config = uvicorn.Config(
        app,
        host=config.host,
        port=config.port,
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()
