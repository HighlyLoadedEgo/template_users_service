from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.application.api.config import AppConfig
from src.application.middlewares.context import set_request_id_middleware
from src.application.middlewares.prometheus import prometheus_metrics_middleware
from src.application.middlewares.structlog import structlog_bind_middleware


def init_middlewares(app: FastAPI, app_config: AppConfig) -> None:
    """Initialize the middlewares for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=structlog_bind_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
    app.add_middleware(BaseHTTPMiddleware, dispatch=prometheus_metrics_middleware)
