from cleanpykit.logging import logger

def test_text_formatter_default():
    log = logger.get_logger("test1", fmt="default", use_color=False)
    record = log.makeRecord("test1", "INFO", "", 0, "Test message", None, None)
    formatted = log.handlers[0].formatter.format(record)
    assert "Test message" in formatted
    assert "\033" not in formatted

def test_text_formatter_color():
    import logging
    log = logger.get_logger("test2", fmt="default", use_color=True)
    record = log.makeRecord("test2", logging.ERROR, "", 0, "Error occurred", None, None)
    formatted = log.handlers[0].formatter.format(record)
    print(formatted)
    assert "Error occurred" in formatted
    assert "\033[91m" in formatted

def test_json_formatter():
    import logging
    log = logger.get_logger("test3", fmt="json")
    record = log.makeRecord("test3", logging.DEBUG, "", 0, "Debugging", None, None)
    formatted = log.handlers[0].formatter.format(record)
    import json
    log_dict = json.loads(formatted)
    assert log_dict["message"] == "Debugging"
    assert log_dict["level"] == "DEBUG"

def test_logger_caching():
    log1 = logger.get_logger("cached_logger", fmt="default", use_color=False)
    log2 = logger.get_logger("cached_logger", fmt="default", use_color=False)
    assert log1 is log2

def test_logger_exception_formatting():
    import logging
    log = logger.get_logger("test_exception", fmt="json")
    try:
        1 / 0
    except ZeroDivisionError:
        record = log.makeRecord("test_exception", logging.ERROR, "", 0, "Division by zero", None, exc_info=logging.sys.exc_info())
        formatted = log.handlers[0].formatter.format(record)
        import json
        log_dict = json.loads(formatted)
        assert "exception" in log_dict
        assert "ZeroDivisionError" in log_dict["exception"]