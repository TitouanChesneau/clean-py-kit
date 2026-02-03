# Changelog

## [0.1.1] - 2026

## [0.1.0] - 2026-02-03
### Added
- YAML config loading with `BaseConfig` and `load_config`
- Flexible logger: text, JSON, and colored formats, with caching
- DI container with `Container` (bind, resolve, override)
- Application with startup and shutdown hooks
- Utility decorators:
  - `singleton`
  - `lazy`
  - `cached`
  - `retry`
  - `timed`
  - `Result` class to handle ok/err operations

### Tests
- Full coverage for utils, logging, config, DI, and app modules