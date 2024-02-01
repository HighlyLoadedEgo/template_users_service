from pydantic import BaseModel


class BrokerConfig(BaseModel):
    host: str = "localhost"
    port: int = 5672
    login: str = "guest"
    password: str = "guest"
