from pydantic import BaseModel

from src.auth.config import JWTConfig
from src.database import DatabaseConfig


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False


class Settings(BaseModel):
    api: ServerConfig
    database: DatabaseConfig
    jwt: JWTConfig
