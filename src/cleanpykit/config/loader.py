import os
import yaml
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
from .env import get_env

T = TypeVar("T", bound=BaseModel)

def load_yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_config(schema: Type[T], base_path: str | None = None) -> T:
    root = base_path or os.getcwd()
    env = get_env()

    base_config = load_yaml(os.path.join(root, "config.yaml"))
    env_config = load_yaml(os.path.join(root, f"config.{env}.yaml"))

    merged = { **base_config, **env_config }
    env_overrides = {
        key.lower(): value
        for key, value in os.environ.items()
        if key.lower() in merged
    }

    merged.update(env_overrides)

    try:
        return schema.model_validate(merged, by_name=True)
    except ValidationError as e:
        raise RuntimeError(f"Invalid configuration: {e}") from e