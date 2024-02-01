import contextlib
import logging
from typing import Optional

import structlog

from src.core.log.processors import build_default_processors


class UvicornDefaultConsoleFormatter(structlog.stdlib.ProcessorFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            processor=structlog.dev.ConsoleRenderer(colors=True),
            foreign_pre_chain=build_default_processors(json_format=False),
        )


class UvicornAccessConsoleFormatter(structlog.stdlib.ProcessorFormatter):
    def __init__(self, *args, **kwargs):
        processors = [
            _extract_uvicorn_request_meta,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ]

        # pass_foreign_args that send values from record.args in positional_args
        super().__init__(
            processors=processors,  # type: ignore
            foreign_pre_chain=build_default_processors(json_format=False),
            pass_foreign_args=True,
        )


class UvicornDefaultJSONFormatter(structlog.stdlib.ProcessorFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            processor=structlog.processors.JSONRenderer(),
            foreign_pre_chain=build_default_processors(json_format=True),
        )


class UvicornAccessJSONFormatter(structlog.stdlib.ProcessorFormatter):
    def __init__(self, *args, **kwargs):
        processors = [
            _extract_uvicorn_request_meta,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ]

        # pass_foreign_args that send values from record.args in positional_args
        super().__init__(
            processors=processors,  # type: ignore
            foreign_pre_chain=build_default_processors(json_format=True),
            pass_foreign_args=True,
        )


def _extract_uvicorn_request_meta(
    wrapped_logger: Optional[logging.Logger], method_name: str, event_dict
):
    """Extract base Uvicron request data."""
    with contextlib.suppress(KeyError, ValueError):
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = event_dict["positional_args"]

        event_dict["client_addr"] = client_addr
        event_dict["http_method"] = method
        event_dict["url"] = full_path
        event_dict["http_version"] = http_version
        event_dict["status_code"] = status_code

        del event_dict["positional_args"]

    return event_dict
