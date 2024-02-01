from pydantic import BaseModel

from src.application.api.config import (
    AppConfig,
    ServerConfig,
)
from src.core.auth.config import JWTConfig
from src.core.database import DatabaseConfig
from src.core.log.config import LoggerConfig
from src.core.message_queue.config import BrokerConfig


class Settings(BaseModel):
    """Compile all settings for this application."""

    server: ServerConfig
    database: DatabaseConfig
    jwt: JWTConfig
    app: AppConfig
    logging: LoggerConfig
    broker: BrokerConfig
