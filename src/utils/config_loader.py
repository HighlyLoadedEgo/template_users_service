import os
import tomllib
from typing import TypeVar, Any
from pydantic import BaseModel, TypeAdapter

ConfigModel = TypeVar('ConfigModel', bound=Any)
DEFAULT_CONFIG_PATH = "./config/config.dev.toml"


def load_config_file(config_path: str) -> dict:
    with open(config_path, "rb") as config_file:
        return tomllib.load(config_file)


def load_config(config_type_model: type[BaseModel]) -> BaseModel:
    config_path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    file_data = load_config_file(config_path=config_path)

    config_adapter = TypeAdapter(type=config_type_model)

    return config_adapter.validate_python(file_data)
