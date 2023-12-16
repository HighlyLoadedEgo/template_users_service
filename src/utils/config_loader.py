import os
import tomllib
from typing import (
    Any,
    TypeVar,
)

from pydantic import (
    BaseModel,
    TypeAdapter,
)

ConfigModel = TypeVar("ConfigModel", bound=Any)
CONFIG_PATH = os.getenv("CONFIG_PATH", "./config/config.dev.toml")


def load_config_file(config_path: str) -> dict:
    """Load config file and return."""
    with open(config_path, "rb") as config_file:
        return tomllib.load(config_file)


def load_config(
    config_type_model: type[BaseModel], config_scope: str | None
) -> BaseModel:
    """Load config file and adapt model type."""
    file_data = load_config_file(config_path=CONFIG_PATH)
    if config_scope is not None:
        file_data = file_data[config_scope]

    config_data = TypeAdapter(type=config_type_model).validate_python(file_data)

    return config_data
