from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.api.config import AppConfig
from src.application.middlewares.apidoc_auth import apidoc_auth_middleware


def init_middlewares(app: FastAPI, app_config: AppConfig) -> None:
    """Initialize the middlewares for the application."""
    if not app_config.local:
        apidoc_auth = apidoc_auth_middleware(app_config=app_config)
        app.add_middleware(apidoc_auth)  # type: ignore

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
