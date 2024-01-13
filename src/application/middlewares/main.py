from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.api.config import AppConfig


def init_middlewares(app: FastAPI, app_config: AppConfig) -> None:
    """Initialize the middlewares for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
