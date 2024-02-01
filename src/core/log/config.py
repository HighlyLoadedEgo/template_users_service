import logging

from pydantic import BaseModel


class LoggerConfig(BaseModel):
    """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """

    level: str | int = logging.INFO
    json_format: bool = False
