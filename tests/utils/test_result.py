import pytest
from cleanpykit.utils import Result

def test_ok_result():
    r = Result(ok=42)
    assert r.is_ok()
    assert not r.is_err()
    assert r.unwrap() == 42

def test_err_result():
    r = Result(err="fail")
    assert r.is_err()
    assert not r.is_ok()
    assert r.unwrap_err() == "fail"

def test_invalid_result():
    with pytest.raises(ValueError):
        Result(ok=1, err="x")

def test_unwrap_err_on_ok():
    r = Result(ok=100)
    with pytest.raises(Exception) as excinfo:
        r.unwrap_err()
    assert "Called unwrap_err on Ok" in str(excinfo.value)

def test_unwrap_on_err():
    r = Result(err="error occurred")
    with pytest.raises(Exception) as excinfo:
        r.unwrap()
    assert "Called unwrap on Err" in str(excinfo.value)