import time
import functools
from typing import Callable, Any, Iterable, Type

def retry(
    exceptions: Iterable[Type[Exception]] = (Exception,),
    tries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            _tries, _delay = tries, delay
            while _tries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    if _tries == 0:
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
        return wrapper
    return decorator