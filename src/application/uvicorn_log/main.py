import logging

from src.application.api.config import ServerConfig
from src.application.uvicorn_log.uvicorn_logger import (
    UvicornAccessConsoleFormatter,
    UvicornAccessJSONFormatter,
    UvicornDefaultConsoleFormatter,
    UvicornDefaultJSONFormatter,
)


def build_uvicorn_log_config(server_config: ServerConfig):
    """Configure Uvicorn logging config."""
    level_name = logging.getLevelName(server_config.log_level)

    if server_config.json_format:
        default = UvicornDefaultJSONFormatter  # type: ignore
        access = UvicornAccessJSONFormatter  # type: ignore
    else:
        default = UvicornDefaultConsoleFormatter  # type: ignore
        access = UvicornAccessConsoleFormatter  # type: ignore

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": default,
            },
            "access": {
                "()": access,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": level_name,
                "propagate": False,
            },
            "uvicorn.error": {
                "level": level_name,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": level_name,
                "propagate": False,
            },
        },
    }
