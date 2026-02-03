import logging
import sys
import json

class TextFormatter(logging.Formatter):
    FORMATS = {
        "default": "[%(asctime)s] [%(name)s] %(message)s",
        "short": "[%(asctime)s] %(message)s [from %(name)s]",
        "date_only": "[%(asctime)s] %(message)s",
    }

    DATE_FORMATS = {
        "default": "%Y-%m-%d %H:%M:%S",
        "short": "%d-%m-%Y %H:%M:%S",
        "date_only": "%m-%d-%Y",
    }

    def __init__(self, fmt_type: str = "default", use_color: bool = False):
        fmt = self.FORMATS.get(fmt_type, self.FORMATS["default"])
        datefmt = self.DATE_FORMATS.get(fmt_type, self.DATE_FORMATS["default"])
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if self.use_color:
            colors = {
                "DEBUG": "\033[94m",
                "INFO": "\033[92m",
                "WARNING": "\033[93m",
                "ERROR": "\033[91m",
                "CRITICAL": "\033[95m",
            }
            color = colors.get(record.levelname, "")
            reset = "\033[0m"
            msg = f"{color}{msg}{reset}"
        return msg

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
        }
        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k not in log_record
            and k not in {"exc_info", "exc_text", "stack_info"}
            and not k.startswith("_")
        }
        log_record.update(extras)
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

_logger_cache: dict[str, logging.Logger] = {}

def get_logger(
    name: str,
    level: str = "DEBUG",
    fmt: str = "default",
    use_color: bool = False
) -> logging.Logger:
    if name in _logger_cache:
        return _logger_cache[name]

    logger = logging.getLogger(name)
    logger.setLevel(level.upper())
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    if fmt == "json":
        formatter = JsonFormatter()
    else:
        formatter = TextFormatter(fmt_type=fmt, use_color=use_color)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    _logger_cache[name] = logger
    return logger