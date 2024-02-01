from src.core.log.config import LoggerConfig
from src.core.log.logger import StructLogger


def configure_logger(logger_config: LoggerConfig) -> None:
    """Configure the logger for the application."""
    struct_logger = StructLogger(
        level=logger_config.level, json_format=logger_config.json_format
    )
    struct_logger.configure()
