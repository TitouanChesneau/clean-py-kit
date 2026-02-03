import os
import pytest

from pybase.config import BaseConfig, load_config

class Config(BaseConfig):
    name: str
    debug: bool = False

def test_valid_config(tmp_path):
    (tmp_path / "config.yaml").write_text("name: app")
    config = load_config(Config, base_path=tmp_path)
    assert config.name == "app"

def test_missing_field(tmp_path):
    (tmp_path / "config.yaml").write_text("")
    with pytest.raises(RuntimeError):
        load_config(Config, base_path=tmp_path)

def test_env_override(tmp_path, monkeypatch):
    (tmp_path / "config.yaml").write_text("name: app")
    monkeypatch.setenv("NAME", "prod")
    config = load_config(Config, base_path=tmp_path)
    assert config.name == "prod"