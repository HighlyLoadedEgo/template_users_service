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
from src.application.metrics_init import init_metrics
from src.application.middlewares.main import init_middlewares
from src.application.routers_init import init_routers
from src.application.uvicorn_log.main import build_uvicorn_log_config
from src.core.log.main import configure_logger
from src.core.utils.config_loader import load_config


def init_app(app_config: AppConfig) -> FastAPI:
    """Initialize the FastAPI application with all dependencies."""
    app = FastAPI(
        debug=app_config.debug, doc_url=None, openapi_url=None, redoc_url=None
    )
    init_swagger_endpoints(app=app, app_config=app_config)
    init_middlewares(app=app, app_config=app_config)
    setup_exception_handlers(app=app)
    init_routers(app=app)
    init_metrics(app=app)

    return app


async def run_api(app: FastAPI, server_config: ServerConfig) -> None:
    """Start the FastAPI application and Uvicorn."""
    log_config = build_uvicorn_log_config(server_config=server_config)
    uvicorn_config = uvicorn.Config(
        app,
        host=server_config.host,
        port=server_config.port,
        log_config=log_config,
    )
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


async def main() -> None:
    """Main entry point."""
    config = load_config(config_type_model=Settings)
    configure_logger(logger_config=config.logging)
    app = init_app(app_config=config.app)
    build_di(app=app, config=config)

    await run_api(server_config=config.server, app=app)
