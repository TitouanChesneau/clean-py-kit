import time
import functools
import inspect
from typing import Callable, Any

def timed(logger=None, label: str | None = None):
    def decorator(func: Callable):
        name = label or func.__name__

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    if logger:
                        logger.info(f"{name} executed in {duration:.4f}s", extra={"duration": duration})
            return async_wrapper
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                if logger:
                        logger.info(f"{name} executed in {duration:.4f}s", extra={"duration": duration})
        return wrapper
    return decorator