from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T, E]):
    def __init__(self, ok: T | None = None, err: E | None = None):
        if (ok is None) == (err is None):
            raise ValueError("Result must have exactly one of ok or err")
        self.ok = ok
        self.err = err

    def is_ok(self) -> bool:
        return self.err is None

    def is_err(self) -> bool:
        return self.err is not None

    def unwrap(self) -> T:
        if self.is_ok():
            return self.ok
        raise Exception(f"Called unwrap on Err: {self.err}")

    def unwrap_err(self) -> E:
        if self.is_err():
            return self.err
        raise Exception(f"Called unwrap_err on Ok: {self.ok}")