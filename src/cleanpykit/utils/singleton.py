from typing import TypeVar, Type, Dict

T = TypeVar("T")

_instances: Dict[Type, object] = {}

def singleton(cls: Type[T]) -> Type[T]:
    def get_instance(*args, **kwargs):
        if not cls in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance