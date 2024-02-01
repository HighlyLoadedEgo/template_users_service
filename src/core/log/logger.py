import logging
import sys

import structlog

from src.core.log.processors import build_default_processors


class StructLogger:
    def __init__(
        self, level: str | int = logging.INFO, json_format: bool = False
    ) -> None:
        self._level = level
        self._json_format = json_format

    def configure(self) -> None:
        """Configure the application logger."""
        self._configure_structlog(self._json_format)
        self._configure_default_logging(
            level=self._level, json_format=self._json_format
        )

    @staticmethod
    def _configure_structlog(json_format: bool) -> None:
        """Set structlog processors and logger factory."""
        structlog.configure_once(
            processors=build_default_processors(json_format=json_format)
            + [
                # used for integration with default logging
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
        )

    @staticmethod
    def _configure_default_logging(*, level: str | int, json_format: bool) -> None:
        """Configure logger format."""
        renderer_processor = (
            structlog.processors.JSONRenderer()
            if json_format
            else structlog.dev.ConsoleRenderer()
        )

        formatter = structlog.stdlib.ProcessorFormatter(
            processors=build_default_processors(json_format=json_format)
            + [
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                renderer_processor,
            ],
        )

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(level)
