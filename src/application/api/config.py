from pydantic import BaseModel

from src.core.auth.config import JWTConfig
from src.core.database import DatabaseConfig


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class AppConfig(BaseModel):
    title: str = "User service"
    version: str = "1.0.0"
    debug: bool = False


class Settings(BaseModel):
    api: ServerConfig
    database: DatabaseConfig
    jwt: JWTConfig
    app: AppConfig
