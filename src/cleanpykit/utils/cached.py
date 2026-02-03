import functools
from typing import Callable, Dict, Tuple, Any

def cached(func: Callable):
    cache: Dict[Tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper