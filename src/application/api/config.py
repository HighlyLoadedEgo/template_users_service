import logging

from pydantic import BaseModel


class ServerConfig(BaseModel):
    """Model of the server configuration."""

    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str | int = logging.DEBUG
    json_format: bool = False


class AppConfig(BaseModel):
    """Model of the application configuration."""

    title: str = "User service"
    version: str = "1.0.0"
    debug: bool = False
    local: bool = True
    doc_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    doc_password: str = "admin"
    doc_username: str = "admin"
    origins: list[str] = ["*"]
