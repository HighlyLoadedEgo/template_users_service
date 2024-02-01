from pydantic import BaseModel


class BaseBrokerMessage(BaseModel):
    extra: dict | None = None
