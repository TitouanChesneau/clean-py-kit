from pybase.utils import retry

def test_retry_success():
    attempts = 0

    @retry(tries=3)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Temporary failure")
        return "Success"

    result = flaky_function()
    assert result == "Success"
    assert attempts == 3

def test_retry_exhaustion():
    attempts = 0

    @retry(tries=2)
    def always_failing_function():
        nonlocal attempts
        attempts += 1
        raise ValueError("Permanent failure")

    try:
        always_failing_function()
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert str(e) == "Permanent failure"
        assert attempts == 2
