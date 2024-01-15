import uvicorn
from fastapi import FastAPI

from src.application.api.config import (
    AppConfig,
    ServerConfig,
    Settings,
)
from src.application.api.exception_handler import setup_exception_handlers
from src.application.api.swagger import init_swagger_endpoints
from src.application.di.di_builder import build_di
from src.application.endpoints_init import init_endpoints
from src.application.middlewares.main import init_middlewares
from src.core.utils.config_loader import load_config


def init_app(app_config: AppConfig) -> FastAPI:
    """Initialize the FastAPI application with all dependencies."""
    app = FastAPI(
        debug=app_config.debug, doc_url=None, openapi_url=None, redoc_url=None
    )
    init_swagger_endpoints(app=app, app_config=app_config)
    init_middlewares(app=app, app_config=app_config)
    setup_exception_handlers(app=app)
    return app


async def run_api(app: FastAPI, server_config: ServerConfig) -> None:
    """Start the FastAPI application and uvicorn."""
    uvicorn_config = uvicorn.Config(
        app,
        host=server_config.host,
        port=server_config.port,
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


async def main() -> None:
    """Main entry point."""
    config = load_config(config_type_model=Settings)

    app = init_app(app_config=config.app)
    build_di(app=app, config=config)
    init_endpoints(app=app)

    await run_api(server_config=config.server, app=app)
