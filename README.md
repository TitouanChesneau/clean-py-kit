# Clean-Py-Kit

## Clean Py Kit : a clean architecture foundation for Python projects

| | |
|-|-|
| Testing | ![Build Status](https://img.shields.io/github/actions/workflow/status/TitouanChesneau/clean-py-kit/tests.yml?branch=master) ![Coverage](https://img.shields.io/codecov/c/gh/TitouanChesneau/clean-py-kit?style=flat-square) | ![PyPI](https://img.shields.io/pypi/v/cleanpykit.svg) ![Downloads](https://img.shields.io/pypi/dm/cleanpykit.svg) |
| Package | ![PyPI version](https://img.shields.io/pypi/v/cleanpykit.svg) ![PyPI downloads](https://img.shields.io/pypi/dm/cleanpykit.svg) ![Status](https://img.shields.io/badge/status-stable-brightgreen) |
| Info    | ![Python version](https://img.shields.io/badge/python-3.10%2B-blue) ![using pytest](https://img.shields.io/badge/tests-pytest-red) [![Github](https://img.shields.io/badge/github-repo-green?logo=github)](https://github.com/TitouanChesneau/clean-py-kit) ![License](https://img.shields.io/badge/license-MIT-blue.svg) |

---

### What is it ?

**Clean-Py-Kit** is a library made to easily structure python projects with a clean architecture.
It provides tools ready to use:

- Config loading from `.yaml` files (`cleanpykit.config`)
- Configurable logging (`cleanpykit.logging`)
- Dependecies injection container (`cleanpykit.di`)
- Application management with startup/shutdown hooks (`cleanpykit.app`)
- Useful utilities : `Result`, `singleton`, `lazy`, `cached`, `retry`, `timed` (`cleanpykit.utils`)

---

## Installation

From PyPI:

```bash
pip install cleanpykit
```

## Minimal Usage

```python
from cleanpykit.config import BaseConfig, load_config
from cleanpykit.logging import get_logger
from cleanpykit.di import Container
from cleanpykit.app import Application
from cleanpykit.utils import singleton, lazy

class Config(BaseConfig):
    log_level: str
    log_use_color: bool = True
    log_format: str = "default"

config = load_config(Config)

log = get_logger(
    __name__,
    level=config.log_level,
    fmt=config.log_format,
    use_color=config.log_use_color
)

container = Container()

@singleton
class Database:
    def __init__(self):
        self.url = "sqlite:///:memory:"

    @lazy
    def client(self):
        return object()

container.bind(Database)

app = Application(container)

def init_db():
    db = container.resolve(Database)
    log.info(f"DB initialized at {db.url}")

app.on_startup(init_db)

def cleanup():
    log.info("Cleanup done")

app.on_shutdown(cleanup)

def main():
    log.info("Application main running")
    db = container.resolve(Database)
    log.info(f"Database URL: {db.url}")

app.run(main)
```

---

## Principals Modules

| **Module** | **Featrues**                                                                                       |
|------------|----------------------------------------------------------------------------------------------------|
| `config`   | Load configuration from YAML files into typed dataclasses.                                         |
| `logging`  | Configurable logging with JSON and colored text formatters.                                        |
| `di`       | Simple dependency injection container for managing class instances.                                |
| `app`      | Application lifecycle management with startup and shutdown hooks.                                  |
| `utils`    | Utility decorators and classes like `Result`, `singleton`, `lazy`, `cached`, `retry`, and `timed`. |

---
